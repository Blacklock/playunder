from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync as ats


class WarfareConsumer(JsonWebsocketConsumer):
    """
    Handles the WebSocket connections for 'Warfare' games.
    self.player - the player object
    self.cult - currently selected cult
    """

    from ._connection import connect, disconnect, receive_json
    from ._page_data import page_data
    from ._home import home_data, create_cult
    from ._contacts import contacts_data, process_choice, option_check

    def user_error(self, error_message, severity='error'):
        """
        Displays an error in the console.
        """
        if severity == 'error':  # Something is wrong, this should not happen
            print('USER_ERROR: ' + error_message + ' [' + self.scope['user'].username + ']')
        elif severity == 'warning':  # Something incorrect happened
            print('USER_WARNING: ' + error_message + ' [' + self.scope['user'].username + ']')


class NotFoundConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print('USER_ERROR: Unknown routing URL!')
        self.close(code=404)
