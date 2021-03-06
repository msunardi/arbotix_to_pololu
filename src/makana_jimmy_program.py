import random
import copy
import subprocess

MaxPosition = [643, 643, 952, 597, 778, 778, 572, 675, 521, 668, 582, 926, 531, 848, 563, 556, 600, 598, 593, 617]
MinPosition = [3,   3,   434, 60,  234, 234, 322, 417, 382, 500, 72,  443, 150, 497, 441, 419, 388, 416, 334, 354]

position_library = {
    'initial_stand': [387,641,460,563,452,572,510,510,-1,510,494,521,498,514,531,488,508,507,509,-1],
    'pause': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'head_to_512': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 512, 512],
    'legs_to_512': [-1, -1, -1, -1, -1, -1, 512, 512, 512, 521, 521, 512, 512, 512, 512, 512, 512, 512, -1, -1],
    'arms_to_512': [512, 512, 512, 512, 512, 512, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'stand': [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512],
    'bow': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 247, 774, -1, -1, -1, -1, -1, -1, -1, -1],
    'head_40_left': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 666, -1], 
    'head_90_left': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 820, -1],
    'head_40_right': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 358, -1],
    'head_90_right': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, -1],
    'look_down': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 370],
    'look_up': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 654],
    'hug': [722, 303, 370, 640, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'raise_arms': [-1, -1, 669, 369, 655, 395, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_arm_wave': [852, -1, 629, -1, 364, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_arm_down': [512, -1, 512, -1, 512, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_arm_wave': [-1, 170, -1, 331, -1, 666, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_arm_down': [-1, 512, -1, 512, -1, 512, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_handshake': [722, -1, 370, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_handshake': [-1, 303, -1, 640, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'sit': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, 820, -1, -1, -1, -1, -1, -1, -1, -1],
    'squat': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, 820, 204, 820, -1, -1, -1, -1, -1, -1],
    'kneeling': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 200, 825, 204, 820, -1, -1, -1, -1, -1, -1, -1],
    'left_lunge': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 650, 820, -1, 800, 675, -1, -1, -1, -1, -1],
    'right_lunge': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, 374, 224, -1, -1, 349, -1, -1, -1, -1],
    'right_splits': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, 204, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_splits': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 820, 820, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_front_kick_40': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 358, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_front_kick_90': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_kick_down': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 512, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_front_kick_40': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 666, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_front_kick_90': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 825, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_kick_down': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 512, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_side_kick_40':[-1, -1, -1, -1, -1, -1, -1, 358, -1, -1, -1, 666, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_side_kick_90': [-1, -1, -1, -1, -1, -1, -1, 358, -1, -1, -1, 820, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_side_kick_down': [-1, -1, -1, -1, -1, -1, -1, 512, -1, -1, -1, 512, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_side_kick_40': [-1, -1, -1, -1, -1, -1, 666, -1, -1, -1, 358, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_side_kick_90': [-1, -1, -1, -1, -1, -1, 666, -1, -1, -1, 204, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_side_kick_down': [-1, -1, -1, -1, -1, -1, 512, -1, -1, -1, 512, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_back_kick_40': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 666, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_back_kick_90': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 820, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_back_kick_40': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 358, -1, -1, -1, -1, -1, -1, -1, -1],
    'left_back_kick_90': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 204, -1, -1, -1, -1, -1, -1, -1, -1],
    'right_knee_up': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 200, -1, 236, -1, -1, -1, -1, -1, -1, -1],
    'left_knee_up': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 825, -1, 799, -1, -1, -1, -1, -1, -1],
    'legs_down': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 512, 512, 512, 512, -1, -1, -1, -1, -1, -1],
    'right_leg_lunge_forward': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 197, 490, 230, 800, 490, 512, -1, -1, -1, -1],
    'left_leg_lunge_forward': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 512, 801, 226, 767, 512, 550, -1, -1, -1, -1],
    'running_start': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 268, 395, 363, -1, -1, -1, -1, -1, -1, -1],
    'running_start_2': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 312, 382, 438, -1, -1, -1, -1, -1, -1, -1],
    'running_right_forward_1': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 374, 518, 438, 730, -1, -1, -1, -1, -1, -1],
    'running_right_forward_2': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 394, 592, 439, 792, -1, -1, -1, -1, -1, -1],
    'running_right_forward_3': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 466, 711, 439, 701, -1, -1, -1, -1, -1, -1],
    'running_left_forward_1': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 598, 711, 385, 652, -1, -1, -1, -1, -1, -1],
    'running_left_forward_2': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 573, 669, 297, 652, -1, -1, -1, -1, -1, -1],
    'running_left_forward_3': [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 447, 621, 255, 652, -1, -1, -1, -1, -1, -1],
    'hands_in_the_air_1': [1019, 3, 363, 661, 509, 515, -1, -1, -1, -1, -1, -1, -1, -1, -1, 562, 562, -1, -1, -1],
    'hands_in_the_air_2': [1019, 3, 363, 661, 509, 515, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'gasp': [705, -1, 486, -1, 283, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    'police_freeze_1': [-1, -1, -1, -1, -1, -1, 504, 511, 513, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, -1],
    'police_freeze_2': [540, 484, 540, 484, 484, 540, 504, 511, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, 507],
    'police_freeze_3': [602, 422, 602, 422, 422, 602, 504, 511, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, 462],
    'police_freeze_4': [668, 356, 668, 356, 356, 668, 504, 511, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, 401],
    'police_freeze_5': [740, 284, 714, 316, 348, 664, 504, 511, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, 401],
    'police_freeze_6': [828, 196, 678, 334, 346, 674, 504, 511, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, 401],
    'police_freeze_7': [-1, -1, 469, 555, 466, 558, 504, 511, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, -1],
    'muscle_flex_1': [-1, -1, -1, -1, 511, -1, -1, -1, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, -1],
    'muscle_flex_2': [830, 518, 469, -1, 322, 681, -1, -1, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, 701, 413],
    'muscle_flex_3': [518, 215, -1, 610, 389, 681, -1, -1, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, 380, 450],
    'muscle_flex_4': [448, 576, -1, -1, -1, -1, -1, -1, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, -1],
    'muscle_flex_5': [848, 176, 660, 364, 511, -1, -1, -1, 503, 522, 228, 798, 502, 528, -1, 513, -1, -1, -1, -1],
    'muscle_flex_6': [848, 176, 660, 364, 273, 757, -1, -1, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, -1],
    'muscle_flex_7': [-1, -1, -1, -1, -1, -1, -1, -1, 503, 522, 228, 798, 236, 778, 502, 528, -1, 513, -1, -1],
    'onguard_1': [388, 639, 459, 562, 452, 569, 517, 506, 508, 515, 513, 500, 497, 515, 527, 495, 506, 508, 507, 510],
    'onguard_2': [388, 639, 459, 562, 452, 569, 517, 506, 508, 515, 405, 500, 498, 515, 433, 495, 524, 508, 507, 510],
    'onguard_3': [388, 639, 459, 562, 452, 569, 517, 492, 537, 508, 288, 428, 387, 524, 422, 371, 505, 488, 507, 510],
    'onguard_4': [390, 631, 459, 561, 451, 570, 600, 566, 507, 506, 349, 424, 395, 538, 472, 394, 516, 489, 506, 510],
    'onguard_5': [675, 756, 464, 575, 506, 520, 600, 566, 507, 506, 349, 424, 395, 538, 472, 394, 516, 489, 506, 510],
    'onguard_6': [675, 756, 464, 575, 506, 520, 600, 566, 507, 506, 349, 424, 395, 538, 472, 394, 516, 489, 409, 510],
    'yes_1': [863, 641, 360, 563, 452, 572, 510, 510, -1, 510, 494, 521, 498, 514, 531, 488, 508, 507, 509, -1],
    'yes_2': [641, 641, 342, 563, 211, 572, 510, 510, -1, 510, 494, 521, 98, 514, 531, 488, 508, 507, 534, 419],
    'yes_3': [682, 641, 342, 563, 231, 572, 510, 510, -1, 510, 494, 521, 498, 514, 531, 488, 508, 507, 534, 502],
    'wow_1': [601, 450, 477, 545, 451, 570, 510, 510, -1, 510, 494, 529, 498, 514, 531, 488, 508, 507, 509, 511],
    'wow_2': [821, 211, 471, 546, 435, 597, 510, 510, -1, 510, 519, 486, 498, 514, 530, 488, 508, 507, 44, 541],
    'wow_3': [897, 162, 561, 686, 391, 649, 467, 465, -1, 510, 519, 486, 498, 514, 531, 488, 508, 50, 598, 582],
    'wow_4': [794, 140, 336, 517, 379, 601, 545, 554, -1, 510, 519, 486, 498, 514, 531, 488, 508, 507, 598, 582],
    'wave_1': [665, 558, 460, 552, 432, 405, 510, 509, -1, 510, 494, 521, 498, 514, 531, 488, 508, 507, 509, -1],
    'wave_2': [919, 558, 368, 55, 385, 405, 510, 509, -1, 533, 478, 498, 498, 514, 531, 488, 508, 50, 509, -1],
    'wave_3': [918, 558, 494, 558, 494, 552, 385, 405, 510, 509, -1, 533, 478, 498, -1, 488, 508, 507, 509, -1],
    'wave_4': [879, 558, 395, 552, 323, 405, 510, 509, -1, 510, 533, 478, 498, 514, 531, 488, 508, 507, 509, -1],
    'wave_5': [918, 558, 494, 552, 385, 405, 510, 509, -1, 510, 515, 500, 598, 514, 531, 488, 508, 507, 509, -1],
    'yawn_1': [556, 641, 461, 563, 418, 572, 510, 510, -1, 510, 494, 521, 498, 514, 531, 488, 508, 507, 509, -1],
    'yawn_2': [783, 641, 233, 563, 351, 572, 510, 510, -1, 510, 494, 521, 498, 514, 531, 488, 508, 507, 508, 577],
    'yawn_3': [724, 641, 425, 563, 387, 572, 510, 510, -1, 510, 494, 521, 498, 514, 531, 488, 508, 507, 508, 577],
    'brah_1': [300, 706, 427, 623, 381, 633, 509, 509, 514, -1, 531, 455, 499, 502, 536, 471, 503, 502, 504, 627],
    'brah_2': [768, 308, 639, 328, 646, 419, 509, 517, 508, 525, 449, 531, 501, 490, 495, 519, 505, 519, 504, 627],
    'brah_3': [488, 289, 473, 729, 499, 709, 511, 495, 505, 537, 419, 598, 424, 631, 533, 455, 500, 536, 506, 359],
    'brah_4': [487, 240, 473, 742, 499, 395, -1, 495, 502, 536, 414, 595, 523, 634, 526, 446, 500, 537, 506, 627],
    'brah_5': [487, 321, 473, 721, 299, 735, -1, 495, 497, 537, 41, 594, 422, 44, 525, 442, 497, 537, 506, 627],
    'brah_6': [487, 247, 473, 719, 499, 438, 511, 495, 497, 537, 414, 591, 422, 646, 523, 437, 498, 537, 506, 627],
    'brah_7': [487, 475, 473, 563, 499, 735, 511, 492, 493, 541, 387, 573, 424, 571, 514, 473, 494, 545, -1, 344],
    'why_1': [832, 613, 192, 561, 370, 570, 522, 511, 524, 52, 203, 734, 42, 979, 755, 186, 498, 504, 506, 348],
    'why_2': [834, 179, 192, 827, 331, 718, 521, 509, 520, 520, 245, 680, 43, 98, 713, 216, 514, -1, 504, 348],
    'why_3': [1023, 7, 396, 645, 538, 507, 521, 508, 521, 522, 251, 675, 43, 976, 709, 221, 523, 521, 646, 627],
    'why_4': [1023, 0, 421, 598, 538, 507, 522, 509, 522, 522, 251, 675, 43, 976, 709, 221, 525, 521, 646, 626],
    'why_5': [1023, 0, 394, 625, 538, 507, 521, 509, 522, 522, 251, 75, 43, 976, 709, 221, 525, 521, 416, 624],
    'why_6': [709, 328, 392, 612, 295, 723, 521, 517, 527, 522, 258, 763, 178, 850, 662, 356, 519, 517, 516, 347],
    'why_7': [460, 580, 426, 590, 497, 503, 518, 519, 505, 537, 471, 544, 513, 490, 515, 516, 497, 533, 518, 347],
    'lookdownup_1': [437, 557, 415, 607, 562, 452, 508, 509, -1, 501, 506, 503, 529, 490, 504, 507, -1, 501, 509, 348],
    'lookdownup_2': [437, 557, 415, 607, 562, 452, 508, 509, -1, 501, 514, 494, 529, 490, 507, 504, -1, 501, 509, 623],
    'lookdownup_3': [434, 561, 415, 607, 563, 451, 519, 490, 522, 506, 534, 474, 529, 490, 528, 487, 516, 506, 513, 344],
    'lookdownup_4': [434, 561, 415, 607, 563, 451, 519, 490, 523, 507, 535, 473, 529, 490, 530, 484, 516, 506, 514, 623],
    'lookdownup_5': [434, 561, 415, 607, 563, 451, 518, 490, 523, 506, 537, 470, 528, 490, 528, 487, 516, 505, 513, 348],
    'lookdownup_6': [434, 561, 415, 607, 563, 451, 518, 490, 523, 506, 539, 467, 529, 490, 532, 482, 516, 504, 513, 626],
    'lookdownup_7': [434, 561, 415, 607, 563, 451, 519, 490, 523, 506, 538, 465, 528, 490, 531, 479, 516, 501, 513, 346],
    'search_1': [413, 568, 397, 620, 493, 511, 508, 508, 505, 521, 533, 492, 528, 490, 530, 502, 503, 524, 510, 351],
    'search_2': [413, 568, 397, 620, 493, 511, 508, 510, 505, 522, 539, 486, 528, 490, 530, 501, 504, 524, 340, 522],
    'search_3': [587, 568, 382, 620, 600, 511, 508, 509, 506, 522, 546, 476, 528, 490, 535, 496, 504, 523, 675, 522],
    'search_4': [614, 568,  479, 620, 597, 511, 508, 509, 507, 522, 549, 472, 528, 490, 534, 494, 505, 523, 448, 522],
    'search_5': [640, 568, 363, 620, 589, 511, 508, 510, 506, 522, 549, 472, 529, 490, 537, 492, 504, 523, 617, 522],
    'search_6': [640, 567, 469, 620, 591, 511, 508, 509, 507, 523, 549, 464, 528, 490, 534, 488, 504, 523, 456, 522],
    'search_7': [657, 568, 337, 620, 573, 511, 508, 510, 507, 523, 552, 459, 528, 490, 533, 485, 503, 522, 687, 521],
    'wave2_1': [1023, 0, 371, 657, 450, 568, 509, 509, 511, 509, 550, 464, 514, 495, 547, 483, 508, 509, 508, 624],
    'wave2_2': [1023, 0, 489, 498, 616, 451, 509, 509, 510, 508, 554, 462, 514, 496, 547, 483, 506, 507, 508, 624],
    'wave2_3': [1023, 0, 372, 647, 616, 451, 433, 419, -1, 523, 506, 461, 529, 490, 496, 476, 504, 517, 508, 624],
    'wave2_4': [1023, 0, 492, 488, 614, 451, 434, 418, -1, 523, 505, 460, 528, 490, 492, 475, 505, 516, 508, 624],
    'wave2_5': [1023, 0, 377, 643, 614, 431, 598, 590, 472, 488, 562, 613, 516, 719, 563, 404, 474, 495, 508, 624],
    'wave2_6': [1023, 0, 503, 514, 617, 431, 597, 589, 472, 488, 562, 613, 516, 721, 567, 398, 473, 494, 508, 624],
    'wave2_7': [983, 36, 382, 559, 452, 570, 509, 509, 505, 505, 520, 482, 500, 493, 521, 511, 500, 500, 508, -1],
    'clap_1': [781, 254, 385, 571, 620, 370, 509, 510, 509, 510, 552, 451, 500, 505, 539, 483, 503, 509, 509, 565],
    'clap_2': [779, 231, 250, 740, 620, 370, 510, 510, 510, 511, 557, 447, 500, 508, 535, 482, 503, 510, 508, 565],
    'clap_3': [814, 234, 417, 556, 687, 380, 508, 509, 511, 510, 554, 446, 517, 498, 523, 486, 505, 507, 508, 564],
    'clap_4': [820, 218, 271, 769, 687, 380, 508, 510, 511, 511, 557, 433, 517, 498, 515, 483, 504, 508, 508, 564],
    'clap_5': [879, 163, 423, 594, 687, 379, 507, 510, 501, -1, 532, 472, 528, 519, 502, 478, 502, 515, 508, 564],
    'clap_6': [867, 174, 254, 752, 688, 373, 508, 510, 504, 514, 537, 457, 528, 518, 503, 470, 502, 514, 508, 564],
    'clap_7': [818, 198, 461, 557, 687, 372, 507, 510, 501, 514, 549, 440, 528, 519, 503, 465, 499, 514, 508, 564],
    'oops_1': [999, 719, 388, 651, 296, 654, 509, 508, 511, 511, 425, 614, 419, 652, 563, 434, 506, 508, 429, 348],
    'oops_2': [1023, 719, 321, 650, 296, 654, 509, 511, -1, 510, 425, 616, 419, 654, 564, 428, 506, 506, 409, 348],
    'oops_3': [955, 719, 315, 650, 296, 654, 509, 510,  511, 426, 614, 419, 659, 564, 424, 506, 506, 433, 348],
    'oops_4': [1023, 719, 314, 650, 295, 654, 508, 511, 511, 510, 433, 613, 419, 671, 569, 414, 503, 502, 473, 348],
    'oops_5': [917, 719, 314, 650, 295, 654, 509, 510, 513, 511, 444, 614, 419, 693, 574, 398, 502, 501, 432, 348],
    'oops_6': [814, 719, 431, 650, 296, 654, 505, 509, 511, 502, 473, 527, 419, 536, 582, 486, 507, 501, 504, 369],   
}


def InsertPositionLibrary(s):
    for key in position_library:
        s[key] = [position_library[key]]

def XMLPositionPair(XML_Out, InitialPosition, NextPosition): #writes the inside of the xml function + calculates step intervals
    
    ServoNames = ['R_SHO_PITCH', 'L_SHO_PITCH', 'R_SHO_ROLL', 'L_SHO_ROLL', 'R_ELBOW', 'L_ELBOW', 'R_HIP_YAW', 'L_HIP_YAW', 'R_HIP_ROLL', 'L_HIP_ROLL', 'R_HIP_PITCH', 'L_HIP_PITCH', 'R_KNEE', 'L_KNEE', 'R_ANK_PITCH', 'L_ANK_PITCH', 'R_ANK_ROLL', 'L_ANK_ROLL', 'HEAD_PAN', 'HEAD_TILT'] 
    Step = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for servo in range(0,20): 
        Step[servo] = (NextPosition[servo] - InitialPosition[servo])/6.0
        print "Step[servo]: %s" % Step[servo]

    print "Initial Position: "
    print InitialPosition
    print "Next Position: "
    print NextPosition
    
    for position in range(0,7):
        XML_Out.write('           <PoseClass>\n')
        XML_Out.write('               <PoseIndex>0</PoseIndex>\n')
        XML_Out.write('               <PoseStep>0</PoseStep>\n')
        XML_Out.write('               <Time>10</Time>\n')
        XML_Out.write('               <PauseTime>0</PauseTime>\n')
        CurrentPosition = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for servo in range(0,20):
            # CurrentPosition[servo] = int(round(InitialPosition[servo] + Step[servo]*position))
            CurrentPosition[servo] = int(round(InitialPosition[servo] + Step[servo]*position))
            XML_Out.write('               <')
            XML_Out.write(ServoNames[servo])
            XML_Out.write('>')
            XML_Out.write(str(CurrentPosition[servo]))
            XML_Out.write('</')
            XML_Out.write(ServoNames[servo])
            XML_Out.write('>\n')
        print CurrentPosition

def XMLPositionList(XML_Out, Positions):
    ServoNames = ['R_SHO_PITCH', 'L_SHO_PITCH', 'R_SHO_ROLL', 'L_SHO_ROLL', 'R_ELBOW', 'L_ELBOW', 'R_HIP_YAW', 'L_HIP_YAW', 'R_HIP_ROLL', 'L_HIP_ROLL', 'R_HIP_PITCH', 'L_HIP_PITCH', 'R_KNEE', 'L_KNEE', 'R_ANK_PITCH', 'L_ANK_PITCH', 'R_ANK_ROLL', 'L_ANK_ROLL', 'HEAD_PAN', 'HEAD_TILT'] 
    XML_Out.write('           <PoseClass>\n')
    XML_Out.write('               <PoseIndex>0</PoseIndex>\n')
    XML_Out.write('               <PoseStep>0</PoseStep>\n')
    XML_Out.write('               <Time>100</Time>\n')
    XML_Out.write('               <PauseTime>50</PauseTime>\n')
    CurrentPosition = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for servo in range(0,20):
        # CurrentPosition[servo] = int(round(InitialPosition[servo] + Step[servo]*position))
        CurrentPosition[servo] = Positions[servo]
        XML_Out.write('               <')
        XML_Out.write(ServoNames[servo])
        XML_Out.write('>')
        XML_Out.write(str(CurrentPosition[servo]))
        XML_Out.write('</')
        XML_Out.write(ServoNames[servo])
        XML_Out.write('>\n')
    print CurrentPosition
    XML_Out.write('           </PoseClass>\n')


def XMLStart(XML_Out): #writes beginning of the xml file
    XML_Out.write('<?xml version="1.0" encoding="utf-8"?>\n<ArrayOfPageClass xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')
    XML_Out.write('   <PageClass>\n')
    XML_Out.write('       <Poses>\n')

def XMLEnd(XML_Out): #writes end of the xml file
    XML_Out.write('       </Poses>\n')
    XML_Out.write('       <Title>RoboArmsInit</Title>\n')
    XML_Out.write('   </PageClass>\n')
    XML_Out.write('</ArrayOfPageClass>\n')
    XML_Out.close()


def MergePositions(CurrentPosition, NextPosition):
    UpdatedNextPosition = copy.copy(NextPosition)
    print "UpdatedNextPosition Before: %s" % UpdatedNextPosition
    for i in range(len(NextPosition)):
        if NextPosition[i] == -1:
                UpdatedNextPosition[i] = CurrentPosition[i]
    print "UpdatedNextPosition After: %s" % UpdatedNextPosition
    return UpdatedNextPosition

def Merge(PositionSequence1, PositionSequence2):  # this merges two sequences
    MergeSequence = []
    l = max(len(PositionSequence1), len(PositionSequence2))
    print "PositionSequence1: %s\nPositionSequence2: %s" % (PositionSequence1, PositionSequence2)
    for i in range(l):
        if i >= len(PositionSequence1):
            MergeSequence = MergeSequence + [PositionSequence2[i]]
        elif i >= len(PositionSequence2):
            MergeSequence = MergeSequence + [PositionSequence1[i]]
        else:
            MergeSequence = MergeSequence + [MergePositions(PositionSequence1[i], PositionSequence2[i])]
    print "MergeSequence: %s" % MergeSequence
    return MergeSequence

def XMLMiddle(XML_Out, PositionSequence):
    print "Pos sequence: %s" % PositionSequence
    CurrentPosition = [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512]
    for i in range(len(PositionSequence)):     
        NextPosition = PositionSequence[i]
        print "NextPosition: %s" % NextPosition
        NextPosition = MergePositions(CurrentPosition, NextPosition)
        if  i != 0:
            # XMLPositionPair(XML_Out, CurrentPosition, NextPosition)
            XMLPositionList(XML_Out, NextPosition)
        CurrentPosition = NextPosition
        print "CurrentPosition: %s" % CurrentPosition

def ProcessPositions(PositionSequence):
    print "Pos sequence: %s" % PositionSequence
    CurrentPosition = [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512]
    output_position = []
    for i in range(len(PositionSequence)):     
        NextPosition = PositionSequence[i]
        print "NextPosition: %s" % NextPosition
        NextPosition = MergePositions(CurrentPosition, NextPosition)
        if  i != 0:
            output_position += [MakePositionList(NextPosition)]
        CurrentPosition = NextPosition
        print "CurrentPosition: %s" % CurrentPosition

    return output_position

def Repeat(n, s):
    if n == 0:
        return []
    else:
        print "s: %s" % s
        return Repeat(n - 1, s) + s

def Random():
    result = []
    for i in range(len(MaxPosition)):
        s = random.randint(MinPosition[i], MaxPosition[i])
        result = result + [s]
    return [result]
    
    
def XMLEverything(XML_Out, PositionSequence): #all the xml stuff put in one def
    XMLStart(XML_Out)
    XMLMiddle(XML_Out, PositionSequence)
    XMLEnd(XML_Out)


def JimmyDo(seq):
    XML_Out = open('TestSequence.pagelist', 'w') #opening the file to write xml info
    XMLEverything(XML_Out, seq)
    # return ProcessPositions(seq)



s = dict()
InsertPositionLibrary(s)
#demo 1:
arm_r = Repeat(3, s['right_arm_wave'] + s['right_arm_down'] + s['muscle_flex_1']) + Repeat(3, s['muscle_flex_1'] + s['right_arm_down'])
arm_l = s['pause'] + Repeat(3, s['left_arm_wave'] + s['left_arm_down'] + s['why_2'] + s['left_arm_down'])
arms = Merge(arm_r, arm_l)
# leg_r = Repeat(2, s['pause']) + Repeat(3, s['right_front_kick_90'] + s['right_kick_down'])
# leg_l = Repeat(3, s['pause']) + Repeat(3, s['left_front_kick_90'] + s['left_kick_down'])
# legs = Merge(leg_r, leg_l)
#squat:
"""arm_r = s['right_handshake']
arm_l = s['left_handshake']
arms = Merge(arm_r, arm_l)
legs = s['pause'] + Repeat(4, s['squat'] + s['legs_down'])"""
#lunge with the left leg forward:
"""arm_r = Repeat(2, s['right_handshake'] + s['arms_to_512'])
arm_l = Repeat(2, s['left_handshake'] + s['arms_to_512'])
arms = Merge(arm_r, arm_l)
legs = Repeat(1, s['left_leg_lunge_forward'] + s['pause'] + s['right_leg_lunge_forward'] + s['stand'])"""
#test random:
"""arm_r = s['right_handshake'] + s['pause'] + Random()
arm_l = s['left_handshake'] + s['pause'] + Random()
arms = Merge(arm_r, arm_l)
leg_r = s['pause'] + s['right_front_kick_40'] + Random()
leg_l = s['pause'] + s['left_front_kick_40'] + Random()
legs = Merge(leg_r, leg_l)"""
#running:
# arms = Repeat(4, s['arms_to_512'])
# legs = s['running_start'] + s['running_start_2'] + Repeat(2, s['running_right_forward_1'] + s['running_right_forward_2'] + s['running_right_forward_3'] + s['running_left_forward_1'] + s['running_left_forward_2'] + s['running_left_forward_3'])

# JimmyDo(s['stand'] + Merge(arms, legs))
print "Arms: %s" % arms
JimmyDo(s['stand'] + arms)
# JimmyDo(s['stand'] + s['right_handshake'] + s['left_handshake'])