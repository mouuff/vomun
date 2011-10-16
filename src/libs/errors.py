class AnonError(Exception):
    pass

class DependancyError(AnonError):
    '''We have an unmet dependancy.'''
    pass

class ConnectionError(AnonError):
    '''Could not connect to a node.'''
    pass
    
class ProtocolError(AnonError):
    '''There was an error parsing the protocol. Maybe we are out of date or
    maybe the node we are connecting to is out of date.'''
    pass
    
class UsageError(AnonError):
    '''You are not properly using the internal code structure or API.
    Check that you are subclassing where possible.'''
    pass