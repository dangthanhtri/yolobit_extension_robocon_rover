const ColorBlock = '#cb2026';
Blockly.Blocks['rover_turn_until_line_detected'] = {
    init: function () {
      this.jsonInit(
        {
          "type": "rover_move_motor",
          "message0": "quay động cơ trái %1 động cơ phải %2 đến khi gặp vạch đen tối đa %3 giây",
          "args0": [
            {
              "type": "input_value",
              "name": "m1_speed",
              "check": "Number",
            },
            {
              "type": "input_value",
              "name": "m2_speed",
              "check": "Number",
            },
            {
              "type": "input_value",
              "name": "second",
              "check": "Number",
            }
          ],
          "inputsInline": true,
          "previousStatement": null,
          "nextStatement": null,
          "colour": ColorBlock,
          "tooltip": "",
          "helpUrl": ""
        }
      );
    }
  };
  
  Blockly.Python["rover_turn_until_line_detected"] = function (block) {
    Blockly.Python.definitions_['import_rover'] = 'from rover import *';
    Blockly.Python.definitions_['import_robocon'] = 'from robot import *';
    var m1_speed = Blockly.Python.valueToCode(block, 'm1_speed', Blockly.Python.ORDER_ATOMIC);
    var m2_speed = Blockly.Python.valueToCode(block, 'm2_speed', Blockly.Python.ORDER_ATOMIC);
    var second = Blockly.Python.valueToCode(block, 'second', Blockly.Python.ORDER_ATOMIC);
    // TODO: Assemble Python into code variable.
    var code = "turn_until_line_detected(" + m1_speed + ", " + m2_speed + "," + second*1000 +")\n";
    return code;
  };

  Blockly.Blocks['rover_follow_line_until'] = {
    init: function () {
      this.jsonInit(
        {
          "type": "rover_follow_line_until",
          "message0": "dò line tốc độ %1 đến khi %2 tối đa %3 giây",
          "args0": [
            {
                type: "input_value",
                check: "Number",
                value: 50,
                name: "speed",             
            },
            {
                "type": "input_value",
                "name": "condition",
            },
            {
                type: "input_value",
                check: "Number",
                name: "timeout",
            }
          ],
          "inputsInline": true,
          "previousStatement": null,
          "nextStatement": null,
          "colour": ColorBlock,
          "tooltip": "",
          "helpUrl": ""
        }
      );
    }
  };
  Blockly.Python["rover_follow_line_until"] = function (block) {
    Blockly.Python.definitions_['import_rover'] = 'from rover import *';
    Blockly.Python.definitions_['import_robocon'] = 'from robot import *';
    var speed = Blockly.Python.valueToCode(block, 'speed', Blockly.Python.ORDER_ATOMIC);
    var condition = Blockly.Python.valueToCode(block, 'condition', Blockly.Python.ORDER_ATOMIC);
    var timeout = Blockly.Python.valueToCode(block, 'timeout', Blockly.Python.ORDER_ATOMIC);
    // TODO: Assemble Python into code variable.
    var code = "follow_line_until ("+ speed +","+ "lambda: (" + condition  + ")" + "," + timeout*1000 +")\n";
    return code;
  };

  
  Blockly.Blocks['rover_follow_line_delay'] = {
    init: function () {
      this.jsonInit(
        {
          "type": "rover_move_delay",
          "message0": "dò line với tốc độ %1 (0-100) trong %2 giây",
          "args0": [
            
            {
              min: 0,
              type: "input_value",
              check: "Number",
              value: 50,
              name: "speed",
            },
            {
              min: 0,
              type: "input_value",
              check: "Number",
              name: "timeout",
            }
          ],
          "inputsInline": true,
          "previousStatement": null,
          "nextStatement": null,
          "colour": ColorBlock,
          "tooltip": "",
          "helpUrl": ""
        }
      );
    }
  };
  
  Blockly.Python["rover_follow_line_delay"] = function (block) {
    Blockly.Python.definitions_['import_rover'] = 'from rover import *';
    Blockly.Python.definitions_['import_robocon'] = 'from robot import *';
    var speed = Blockly.Python.valueToCode(block, 'speed', Blockly.Python.ORDER_ATOMIC);
    var timeout = Blockly.Python.valueToCode(block, 'timeout', Blockly.Python.ORDER_ATOMIC);
    // TODO: Assemble Python into code variable.
    var code =  "follow_line_delay(" + speed + ", " + timeout *1000 + ")\n";
    return code;
  };
