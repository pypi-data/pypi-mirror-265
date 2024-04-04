import json
import jsonref
import inflection
from typing import List
from .action import Action
from .trigger import AlreadyExistsError, Trigger
    
def add_tool_name(tool_name: str, action_name: str) -> str:
    return f"{tool_name.lower()}_{inflection.underscore(action_name)}"

class Tool():
    _custom_id: str = "default"  # Add an internal variable to hold the custom repo name

    @property
    def custom_id(self) -> str:
        return self._custom_id
    
    @custom_id.setter
    def custom_id(self, value: str):
        self._custom_id = value  # Set the internal variable

    def identifier_name(self) -> str:
        return f"{self.__class__.__name__.lower()}_{self.custom_id}"

    def actions(self) -> List[Action]:
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def triggers(self) -> List[Trigger]:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def execute_action(self, action_name: str, request_data: dict, authorisation_data: dict) -> dict:
        tool_name = self.__class__.__name__
        for action in self.actions():
            action_name_shared = add_tool_name(tool_name, action.__name__)
            if action_name_shared == action_name:
                print(f"Executing {action.__name__} on Tool: {tool_name} with request data {request_data} and authorisation data {authorisation_data}")
                try:
                    request_schema = action().request_schema
                    req = request_schema.model_validate_json(json_data=json.dumps(request_data))
                    return action().execute(req, authorisation_data)
                except Exception as e:
                    print(f"Error executing {action.__name__} on Tool: {tool_name}: {e}")
                    return {"status": "failure", "details": str(e)}
        return {"status": "failure", "details": "Action not found"}
    
    def set_webhook_url(self, trigger_name: str, authorisation_data: dict, trigger_config: dict) -> dict: 
        tool_name = self.__class__.__name__
        for trigger in self.triggers():
            trigger_name_shared = add_tool_name(tool_name, trigger.__name__)
            if trigger_name_shared == trigger_name:
                print(f"Setting webhook URL for Trigger: {trigger_name} on Tool: {tool_name} with URL {trigger_config['webhook_url']} and authorisation data {authorisation_data}")
                try:
                    webhook_url = trigger_config["webhook_url"]
                    del trigger_config["webhook_url"]
                    trigger_config_schema = trigger().trigger_config_schema
                    tc = trigger_config_schema.model_validate_json(json_data=json.dumps(trigger_config))
                    conn_data = trigger().set_webhook_url(authorisation_data, webhook_url, tc)
                    return {"status": "success", "connection_data": conn_data}
                except AlreadyExistsError as e:
                    print(f"Webhook URL already exists for Trigger: {trigger_name} on Tool: {tool_name}: {e}")
                    return {"status": "failure", "details": "Webhook URL already exists"}
                except Exception as e:
                    print(f"Error setting webhook URL for Trigger: {trigger_name} on Tool: {tool_name}: {e}")
                    return {"status": "failure", "details": str(e)}
        return {"status": "failure", "details": "Trigger not found"}
    
    def transform_trigger_payload(self, payload: dict) -> dict:
        tool_name = self.__class__.__name__
        for trigger in self.triggers():
            try:
                print(f"Transforming trigger payload for Tool: {tool_name}")
                (match, connection_data, converted_payload) = trigger().check_and_convert_to_identifier_payload_schema(payload)
                print(f"Match: {match}, Connection Data: {connection_data}, Converted Payload: {converted_payload}")
                if match:
                    return {
                        "trigger_name": add_tool_name(tool_name, trigger.__name__),
                        "connection_data": connection_data,
                        "payload": converted_payload
                    }
            except Exception as e:
                print(f"Error transforming trigger payload for Tool: {tool_name}: {str(e)}")
        return {"status": "failure", "details": "Trigger not found"}
        
        
    def json_schema(self):
        tool_name = self.__class__.__name__
        return {
            "Name": tool_name,
            "Description": self.__doc__.strip() if self.__doc__ else None,
            "CustomID": self.custom_id,
            "Actions": [
                {
                    "name": add_tool_name(tool_name, action.__name__),
                    "display_name": action().display_name,
                    "description": action.__doc__.strip() if action.__doc__ else None,
                    "parameters": jsonref.loads(json.dumps(action().request_schema.model_json_schema())),
                    "response": jsonref.loads(json.dumps(action().response_schema.model_json_schema()))
                } for action in self.actions()
            ],
            "Triggers": [
                {
                    "name": add_tool_name(tool_name, trigger.__name__),
                    "display_name": trigger().display_name,
                    "description": trigger.__doc__.strip() if trigger.__doc__ else None,
                    "payload": jsonref.loads(json.dumps(trigger().payload_schema.model_json_schema())),
                    "config": jsonref.loads(json.dumps(trigger().trigger_config_schema.model_json_schema())),
                    "instructions": trigger().trigger_instructions
                } for trigger in self.triggers()
            ],
        }


