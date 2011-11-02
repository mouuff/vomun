from libs.construct import *


DUMP_ALL_PACKETS = False

packets = {
    0:  Struct("ConnectionRequest",
            Enum(UBInt32("encryptionmethod"),
                rsa=0,
                aes=1,
            ),
            UBInt32("iplength"),
            MetaField("ip", lambda ctx: ctx["iplength"]),
            UBInt32("keylength"),
            MetaField("key", lambda ctx: ctx["keylength"])        
        ),

    1:  Struct("Disconnect",
            Enum(UBInt32("reasonType"),
                NoReason=0,
                HoldOff=1,
                Disconnect=2,
                Custom=3),
            UBInt32("reasonlength"),
            MetaField("reason", lambda ctx: ctx["reasonlength"]),
        ),
    2:  Struct("AcceptConnection",
            UBInt8("int")
        ),

    3:  Struct("Message"),
            UBInt32("to_node_length"),
            MetaField("to_node", lambda ctx: ctx["to_node_length"]),
            UBInt32("timestamp"),
            UBInt32("message_length"),
            MetaField("message", lambda ctx: ctx["message_length"])
        )    
        
}



packet_stream = Struct("packet_stream",
    OptionalGreedyRange(
        Struct("full_packet",
            UBInt8("header"),
            Switch("payload", lambda context: context["header"], packets),
        ),
    ),
    OptionalGreedyRange(
        UBInt8("leftovers"),
    ),
)

packets_by_name = dict((v.name, k) for (k, v) in packets.iteritems())
packets_by_id = dict((k, v.name) for (k, v) in packets.iteritems())


def make_packet(packet, *args, **kwargs):
    """
    Constructs a packet bytestream from a packet header and payload.

    The payload should be passed as keyword arguments. Additional containers
    or dictionaries to be added to the payload may be passed positionally, as
    well.
    """

    if packet not in packets_by_name:
        print("Couldn't find packet name %s!" % packet)
        return ""

    header = packets_by_name[packet]

    for arg in args:
        kwargs.update(dict(arg))
    container = Container(**kwargs)

    if DUMP_ALL_PACKETS:
        print("Making packet %s (%d)" % (packet, header))
        print(container)
    payload = packets[header].build(container)
    return chr(header) + payload


def parse_packets(bytestream):
    """
    Opportunistically parse out as many packets as possible from a raw
    bytestream.

    Returns a tuple containing a list of unpacked packet containers, and any
    leftover unparseable bytes.
    """

    container = packet_stream.parse(bytestream)

    l = [(i.header, i.payload) for i in container.full_packet]
    leftovers = "".join(chr(i) for i in container.leftovers)

    if DUMP_ALL_PACKETS:
        for packet in l:
            print("Parsed packet %d" % packet[0])
            print(packet[1])

    return l, leftovers