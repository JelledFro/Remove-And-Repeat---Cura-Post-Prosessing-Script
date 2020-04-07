# adds code for cooling down and moving between up to 4 positions, to wipe the model of the print bed and make place for another
# then copies the entire GCODE files content n nr of times to print aditional identical models in a row

from ..Script import Script

class RemoveAndRepeat(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Remove and repeat print",
            "key": "RemoveAndRepeat",
            "metadata":{},
            "version": 2,
            "settings":
            {
                "number_of_prints":
                {
                    "label": "Number of repeats",
                    "type": "int",
                    "minimum_value": "1",
                    "default_value": 2
                },
                "cool_between_prints":
                {
                    "label": "cool bed and tool between prints",
                    "type": "bool",
                    "default_value": true
                }, 
                "tool_temp":
                {
                    "label": "hot end cool down temperature",
                    "unit": "°C",
                    "type" : "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cool_between_prints"
                },
                "bed_temp":
                {
                    "label": "bed cool down temperature",
                    "unit": "°C",
                    "type" : "float",
                    "default_value": 30.0,
                    "minimum_value": "0",
                    "enabled": "cool_between_prints"
                },
                "cool_Z":
                {
                    "label": "Z position for cooling",
                    "description": "At what height should the print head wait while it cools?",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 50,
                    "enabled": "cool_between_prints"
                },
                "cool_X":
                {
                    "label": "X position for cooling",
                    "description": "What X location does the head move to when pausing.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0,
                    "enabled": "cool_between_prints"
                },
                "cool_Y":
                {
                    "label": "Y position for cooling",
                    "description": "What Y location does the head move to when pausing.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0,
                    "enabled": "cool_between_prints"
                },
                "pos_1_X":
                {
                    "label": "Position 1, X coordinate",
                    "description": "X value for position 1.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_1_Y":
                {
                    "label": "Position 1, Y coordinate",
                    "description": "Y value for position 1.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0,
                },
                "pos_1_Z":
                {
                    "label": "Position 1, Z coordinate",
                    "description": "Z value for position 1.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 50
                },
                "pos_2_X":
                {
                    "label": "Position 2, X coordinate",
                    "description": "X value for position 2.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_2_Y":
                {
                    "label": "Position 2, Y coordinate",
                    "description": "Y value for position 2.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_2_Z":
                {
                    "label": "Position 2, Z coordinate",
                    "description": "Z value for position 2.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.4
                },
                "pos_3_X":
                {
                    "label": "Position 3, X coordinate",
                    "description": "X value for position 3.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_3_Y":
                {
                    "label": "Position 3, Y coordinate",
                    "description": "Y value for position 3.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_3_Z":
                {
                    "label": "Position 3, Z coordinate",
                    "description": "Z value for position 3.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.4
                },
                "pos_4_X":
                {
                    "label": "Position 4, X coordinate",
                    "description": "X value for position 4.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_4_Y":
                {
                    "label": "Position 4, Y coordinate",
                    "description": "Y value for position 4.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_4_Z":
                {
                    "label": "Position 4, Z coordinate",
                    "description": "Z value for position 4.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.4
                },
                "pos_5_X":
                {
                    "label": "Position 5, X coordinate",
                    "description": "X value for position 5.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_5_Y":
                {
                    "label": "Position 5, Y coordinate",
                    "description": "Y value for position 5.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "pos_5_Z":
                {
                    "label": "Position 5, Z coordinate",
                    "description": "Z value for position 5.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0.4
                }
            }
        }"""

    def execute(self, data):
        cool = self.getSettingValueByKey("cool_between_prints")
        tool_temp = self.getSettingValueByKey("tool_temp")
        bed_temp = self.getSettingValueByKey("bed_temp")
        cool_Z = self.getSettingValueByKey("cool_Z")
        cool_X = self.getSettingValueByKey("cool_X")
        cool_Y = self.getSettingValueByKey("cool_Y")
        X1 = self.getSettingValueByKey("pos_1_X")
        Y1 = self.getSettingValueByKey("pos_1_Y")
        Z1 = self.getSettingValueByKey("pos_1_Z")
        X2 = self.getSettingValueByKey("pos_2_X")
        Y2 = self.getSettingValueByKey("pos_2_Y")
        Z2 = self.getSettingValueByKey("pos_2_Z")
        X3 = self.getSettingValueByKey("pos_3_X")
        Y3 = self.getSettingValueByKey("pos_3_Y")
        Z3 = self.getSettingValueByKey("pos_3_Z")
        X4 = self.getSettingValueByKey("pos_4_X")
        Y4 = self.getSettingValueByKey("pos_4_Y")
        Z4 = self.getSettingValueByKey("pos_4_Z")
        X5 = self.getSettingValueByKey("pos_5_X")
        Y5 = self.getSettingValueByKey("pos_5_Y")
        Z5 = self.getSettingValueByKey("pos_5_Z")

        end_code = ""
        end_code += self.putValue(M = 300, P = 200, S = 1500) + "\n"

        if cool:
            end_code += self.putValue(G = 0, X = cool_X , Y = cool_Y, Z = cool_Z) + "\n"
            end_code += self.putValue(M = 106, P = 0) + ";turns on fans to increase cooling" + "\n"
            end_code += self.putValue(M = 106, P = 1) + "\n"
            end_code += self.putValue(M = 106, P = 2) + "\n"
            end_code += self.putValue(M = 109, R = tool_temp) + ";wait for hotend to cool" +"\n"
            end_code += self.putValue(M = 190, R = bed_temp) + ";wait for bed to cool" +"\n"
            end_code += self.putValue(M = 300, P = 200, S = 1700) + "\n"
            end_code += self.putValue(M = 300, P = 200, S = 1700) + "\n"

        end_code += ";moves\n"
        # end_code += self.putValue(M = 117, "removing print") + "\n"
        end_code += self.putValue(G = 0, X = X1 , Y = Y1, Z = Z1) + "\n"
        end_code += self.putValue(G = 0, X = X2 , Y = Y2, Z = Z2) + "\n"
        end_code += self.putValue(G = 0, X = X3 , Y = Y3, Z = Z3) + "\n"
        end_code += self.putValue(G = 0, X = X4 , Y = Y4, Z = Z4) + "\n"
        end_code += self.putValue(G = 0, X = X5 , Y = Y5, Z = Z5) + "\n"


        end_code += self.putValue(M = 300, P = 200, S = 2200) + "\n"
        end_code += self.putValue(M = 300, P = 200, S = 2200) + "\n"
        end_code += self.putValue(M = 300, P = 200, S = 2200) + "\n"

        end_code += ";end of print\n"
        data += end_code

        number_of_printes = self.getSettingValueByKey("number_of_prints")
        
        repeat = data

        i = 1
        while i < number_of_printes:
            data += repeat
            i += 1

        return data
