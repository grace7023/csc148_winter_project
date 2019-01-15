"""
constants needed for stonehenge module
"""

from typing import Dict, List, Tuple


LETTERS_ROW = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXY']

LETTERS_T1 = [x for x in 'BCA']
LETTERS_T2 = [x for x in 'EGBDFAC']
LETTERS_T3 = [x for x in 'ILEHKBDGJACF']
LETTERS_T4 = [x for x in 'NRIMQEHLPBDGKOACFJ']
LETTERS_T5 = [x for x in 'TYNSXIMRWEHLQVBDGKPUACFJO']

LETTERS_TLIST = [LETTERS_T1, LETTERS_T2, LETTERS_T3, LETTERS_T4, LETTERS_T5]


LETTERS_B1 = [x for x in 'ACB']
LETTERS_B2 = [x for x in 'CFADGBE']
LETTERS_B3 = [x for x in 'FJCGKADHLBEI']
LETTERS_B4 = [x for x in 'JOFKPCGLQADHMRBEIN']
LETTERS_B5 = [x for x in 'OUJPVFKQWCGLRXADHMSYBEINT']

LETTERS_BLIST = [LETTERS_B1, LETTERS_B2, LETTERS_B3, LETTERS_B4, LETTERS_B5]


def generate_leylines(n: int) -> Tuple[Dict[str, List[object]],
                                       Dict[str, List[object]]]:
    """
    Return a tuple with two dictionaries. Each has three keys, indicating the
    leylines for each direction (horizontal, diagonal down to the left,
    diagonal down to the right) depending on sidelength n. The first dictionary
    is for the letter nodes, while the second is for the leylines.

    >>> t = generate_leylines(2)
    >>> all([t[0]['r'][0] == ['A', 'B'], t[1]['r'] == ['@', '@', '@']])
    True
    """
    lists_ = list()
    lists_.append(LETTERS_ROW)
    lists_.append(LETTERS_TLIST[n - 1])
    lists_.append(LETTERS_BLIST[n - 1])
    total1 = {}
    total2 = {}
    total_keys = ['r', 't', 'b']
    for j in range(3):
        # letter leylines
        num_list = [x * (x + 1) // 2 - 1 for x in range(1, n + 2)]
        letter_list = [[lists_[j][i] for i in range(num_list[k],
                                                    num_list[k + 1])]
                       for k in range(len(num_list) - 1)]
        letter_list.append(
            [lists_[j][i] for i in range(num_list[-1], num_list[-1] + n)])
        total1[total_keys[j]] = letter_list
        # key leylines
        letter_list = ['@' for _ in range(j * (n + 1), j * (n + 1) + n + 1)]
        total2[total_keys[j]] = letter_list
    return (total1, total2)


GRID_1 = """      {0[t][1]}   {0[t][0]}
     /   /
{0[r][0]} - {1[0]} - {1[1]}
     \\ / \\
  {0[r][1]} - {1[2]}   {0[b][1]}
       \\
        {0[b][0]}"""

GRID_2 = """        {0[t][2]}   {0[t][1]}
       /   /
  {0[r][0]} - {1[0]} - {1[1]}   {0[t][0]}
     / \\ / \\ /
{0[r][1]} - {1[2]} - {1[3]} - {1[4]}
     \\ / \\ / \\
  {0[r][2]} - {1[5]} - {1[6]}   {0[b][2]}
       \\   \\
        {0[b][0]}   {0[b][1]}"""

GRID_3 = """          {0[t][3]}   {0[t][2]}
         /   /
    {0[r][0]} - {1[0]} - {1[1]}   {0[t][1]}
       / \\ / \\ /
  {0[r][1]} - {1[2]} - {1[3]} - {1[4]}   {0[t][0]}
     / \\ / \\ / \\ /
{0[r][2]} - {1[5]} - {1[6]} - {1[7]} - {1[8]}
     \\ / \\ / \\ / \\
  {0[r][3]} - {1[9]} - {1[10]} - {1[11]}   {0[b][3]}
       \\   \\   \\
        {0[b][0]}   {0[b][1]}   {0[b][2]}"""

GRID_4 = """            {0[t][4]}   {0[t][3]}
           /   /
      {0[r][0]} - {1[0]} - {1[1]}   {0[t][2]}
         / \\ / \\ /
    {0[r][1]} - {1[2]} - {1[3]} - {1[4]}   {0[t][1]}
       / \\ / \\ / \\ /
  {0[r][2]} - {1[5]} - {1[6]} - {1[7]} - {1[8]}   {0[t][0]}
     / \\ / \\ / \\ / \\ /
{0[r][3]} - {1[9]} - {1[10]} - {1[11]} - {1[12]} - {1[13]}
     \\ / \\ / \\ / \\ / \\
  {0[r][4]} - {1[14]} - {1[15]} - {1[16]} - {1[17]}   {0[b][4]}
       \\   \\   \\   \\
        {0[b][0]}   {0[b][1]}   {0[b][2]}   {0[b][3]}
        """

GRID_5 = """              {0[t][5]}   {0[t][4]}
             /   /
        {0[r][0]} - {1[0]} - {1[1]}   {0[t][3]}
           / \\ / \\ /
      {0[r][1]} - {1[2]} - {1[3]} - {1[4]}   {0[t][2]}
         / \\ / \\ / \\ /
    {0[r][2]} - {1[5]} - {1[6]} - {1[7]} - {1[8]}   {0[t][1]}
       / \\ / \\ / \\ / \\ / 
  {0[r][3]} - {1[9]} - {1[10]} - {1[11]} - {1[12]} - {1[13]}   {0[t][0]}
     / \\ / \\ / \\ / \\ / \\ / 
{0[r][4]} - {1[14]} - {1[15]} - {1[16]} - {1[17]} - {1[18]} - {1[19]}
     \\ / \\ / \\ / \\ / \\ / \\
  {0[r][5]} - {1[20]} - {1[21]} - {1[22]} - {1[23]} - {1[24]}   {0[b][5]}
       \\   \\   \\   \\   \\
        {0[b][0]}   {0[b][1]}   {0[b][2]}   {0[b][3]}   {0[b][4]}
        """

GRIDS = [GRID_1, GRID_2, GRID_3, GRID_4, GRID_5]
