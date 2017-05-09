#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#

WIKIHOUSE_1 = '14/2/61'
WIKIHOUSE_2 = '14/2/56'
WIKIHOUSE_3 = '14/2/51'
Couloir = '14/2/166'
SQUAD_1 = '14/2/131'
SQUAD_2 = '14/2/121'
SQUAD_3 = '14/2/111'

RADIUS = 1

RGB_FIRST_KNX = '14/3/1'
RGB_TOTAL = 12
RGB_STEP = 20

LED_FIRST_KNX = '14/2/11'
LED_TOTAL = 14
LED_STEP = 5

CHRISTMAS_COLORS = [[200, 30, 40, 0],
                    [0, 150, 70, 0],
                    [205, 155, 0, 0]
                    ]

DSL_MOTION_SENSORS = [['000070B3D5C1503F', 'Cafe'],
                      ['000070B3D5C15046', 'Squad_1'],
                      ['000070B3D5C15071', 'Squad_2'],
                      ['000070B3D5C15048', 'Squad_3'],
                      ['000070B3D5C15041', 'Squad_4'],
                      ['000070B3D5C15045', 'Wiki_1'],
                      ['000070B3D5C150A4', 'Wiki_2'],
                      ['000070B3D5C15043', 'Wiki_3'],
                      ['000070B3D5C15044', 'Homy'],
                      ['000070B3D5C15042', 'Tetris']
                      ]


#      / \
#     Y | # # # # #       SDL MAP         # # # # #
#       | # # # # #                       # # # # #
#       | # # # # #                       # # # # #
#       | # # # # #                       # # # # #
#       | # # # # #                 # # # # # # # #
#       | # # # # # # #             # # # # # # # #
#       | # # # # # # #             # # # # # # # #
#       | # # # # # # #             # # # # # # # #
#       | # # # # # # # # # # # # # # # # # # # # #
#       | # # # # # # # # # # # # # # # # # # # # #
#       | # # # # # # # # # # # # # # # # # # # # #
#       | # # # # # # # # # # # # # # # # # # # # #
#       | # # # # # # # # # # # # # # # # # # # # #
#     --|------------------------------------------->  X
#       |

X = 15
Y = 11

LED_POSITION = [[0, 0, 'SQUAD_2_A'],
                [0, 1, 'SQUAD_2_A'],
                [0, 2, 'SQUAD_2_B'],
                [0, 3, 'SQUAD_2_B'],
                [0, 4, 'WIKIHOUSE_3'],
                [0, 5, 'WIKIHOUSE_3'],
                [0, 6, 'SQUAD_1_B'],
                [0, 7, 'SQUAD_1_B'],
                [0, 8, 'SQUAD_1_B'],
                [0, 9, 'SQUAD_1_B'],
                [0, 10, 'SQUAD_1_B'],

                [1, 0, 'SQUAD_2_A'],
                [1, 1, 'SQUAD_2_A'],
                [1, 2, 'SQUAD_2_B'],
                [1, 3, 'SQUAD_2_B'],
                [1, 4, 'WIKIHOUSE_3'],
                [1, 5, 'WIKIHOUSE_3'],
                [1, 6, 'SQUAD_1_B'],
                [1, 7, 'SQUAD_1_B'],
                [1, 8, 'SQUAD_1_B'],
                [1, 9, 'SQUAD_1_B'],
                [1, 10, 'SQUAD_1_B'],

                [2, 0, 'WIKIHOUSE_2'],
                [2, 1, 'WIKIHOUSE_2'],
                [2, 2, 'WIKIHOUSE_2'],
                [2, 3, 'SQUAD_2_B'],
                [2, 4, 'WIKIHOUSE_3'],
                [2, 5, 'WIKIHOUSE_3'],
                [2, 6, 'SQUAD_1_B'],
                [2, 7, 'SQUAD_1_B'],
                [2, 8, 'SQUAD_1_B'],
                [2, 9, 'SQUAD_1_B'],
                [2, 10, 'SQUAD_1_B'],

                [3, 0, 'WIKIHOUSE_2'],
                [3, 1, 'WIKIHOUSE_2'],
                [3, 2, 'WIKIHOUSE_2'],
                [3, 3, 'COULOIR_C'],
                [3, 4, 'COULOIR_D'],
                [3, 5, 'COULOIR_D'],
                [3, 6, 'COULOIR_D'],

                [4, 0, 'SQUAD_3_A'],
                [4, 1, 'SQUAD_3_B'],
                [4, 2, 'SQUAD_3_B'],
                [4, 3, 'COULOIR_C'],

                [5, 0, 'SQUAD_3_A'],
                [5, 1, 'SQUAD_3_B'],
                [5, 2, 'SQUAD_3_B'],
                [5, 3, 'COULOIR_C'],

                [6, 0, 'SQUAD_3_A'],
                [6, 1, 'SQUAD_3_B'],
                [6, 2, 'SQUAD_3_B'],
                [6, 3, 'COULOIR_B'],

                [7, 0, 'SQUAD_3_A'],
                [7, 1, 'SQUAD_3_B'],
                [7, 2, 'SQUAD_3_B'],
                [7, 3, 'COULOIR_B'],
                [7, 4, 'COULOIR_A'],
                [7, 5, 'COULOIR_A'],

                [8, 0, 'WIKIHOUSE_1'],
                [8, 1, 'WIKIHOUSE_1'],
                [8, 2, 'WIKIHOUSE_1'],
                [8, 3, 'ACCEUIL_D'],
                [8, 4, 'ACCEUIL_B'],
                [8, 5, 'ACCEUIL_B'],

                [9, 0, 'WIKIHOUSE_1'],
                [9, 1, 'WIKIHOUSE_1'],
                [9, 2, 'WIKIHOUSE_1'],
                [9, 3, 'ACCEUIL_D'],
                [9, 4, 'ACCEUIL_D'],
                [9, 5, 'ACCEUIL_B'],

                [10, 0, 'PRESENTATION_G'],
                [10, 1, 'PRESENTATION_H'],
                [10, 2, 'PRESENTATION_H'],
                [10, 3, 'ACCEUIL_C'],
                [10, 4, 'ACCEUIL_A'],
                [10, 5, 'ACCEUIL_A'],

                [11, 0, 'PRESENTATION_G'],
                [11, 1, 'PRESENTATION_G'],
                [11, 2, 'PRESENTATION_H'],
                [11, 3, 'ACCEUIL_C'],
                [11, 4, 'ACCEUIL_C'],

                [12, 0, 'PRESENTATION_F'],
                [12, 1, 'PRESENTATION_F'],
                [12, 2, 'PRESENTATION_D'],
                [12, 3, 'PRESENTATION_D'],
                [12, 4, 'PRESENTATION_A'],
                [12, 5, 'PRESENTATION_A'],
                [12, 6, 'SQUAD_4_B'],

                [13, 0, 'PRESENTATION_E'],
                [13, 1, 'PRESENTATION_F'],
                [13, 2, 'PRESENTATION_D'],
                [13, 3, 'PRESENTATION_C'],
                [13, 4, 'PRESENTATION_A'],
                [13, 5, 'PRESENTATION_B'],
                [13, 6, 'SQUAD_4_B'],

                [14, 0, 'PRESENTATION_E'],
                [14, 1, 'PRESENTATION_E'],
                [14, 2, 'PRESENTATION_C'],
                [14, 3, 'PRESENTATION_C'],
                [14, 4, 'PRESENTATION_B'],
                [14, 5, 'PRESENTATION_B'],
                [14, 6, 'SQUAD_4_A']
                ]

LORA_SENSOR = [['A81758FFFE03045F', 'PRESENTATION'],
               ['A81758FFFE030460', 'Acceuil'],
               ['A81758FFFE030461', 'Squad_3'],
               ['A81758FFFE030425', 'Squad_2'],
               ['A81758FFFE0303FC', 'Squad_1'],
               ['A81758FFFE0301CC', 'WIKIHOUSE_1'],
               ['A81758FFFE0304B5', 'WIKIHOUSE_2'],
               ['A81758FFFE0304B7', 'WIKIHOUSE_3']
                ]


LIGHT_LOOKUP_TABLE = [['SQUAD_3_A', '14/2/11', 1],
                    ['SQUAD_3_B', '14/2/16', 1],
                    ['SQUAD_2_A', '14/2/21', 1],
                    ['SQUAD_2_B', '14/2/26', 1],
                    ['SQUAD_1_A', '14/2/31', 1],
                    ['SQUAD_1_B', '14/2/36', 1],
                    ['SQUAD_4_A', '14/2/41', 1],
                    ['SQUAD_4_B', '14/2/46', 1],
                    ['WIKIHOUSE_1', '14/2/51', 1],
                    ['WIKIHOUSE_2', '14/2/56', 1],
                    ['WIKIHOUSE_3', '14/2/61', 1],
                    ['COULOIR_A', '14/2/66', 1],
                    ['COULOIR_B', '14/2/71', 1],
                    ['COULOIR_C', '14/2/76', 1],
                    ['COULOIR_D', '14/2/81', 1],

                    ['ACCEUIL_A', '14/3/1', 4],
                    ['ACCEUIL_B', '14/3/21', 4],
                    ['ACCEUIL_C', '14/3/41', 4],
                    ['ACCEUIL_D', '14/3/61', 4],
                    ['PRESENTATION_A', '14/3/81', 4],
                    ['PRESENTATION_B', '14/3/101', 4],
                    ['PRESENTATION_C', '14/3/121', 4],
                    ['PRESENTATION_D', '14/3/141', 4],
                    ['PRESENTATION_E', '14/3/161', 4],
                    ['PRESENTATION_F', '14/3/181', 4],
                    ['PRESENTATION_G', '14/3/201', 4],
                    ['PRESENTATION_H', '14/3/221', 4]
                    ]

