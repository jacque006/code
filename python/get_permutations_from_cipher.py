"""


'1' -> 'a'
'2' -> 'b'
...
'11' -> 'k'
...
'26' -> 'z'


'11' -> 'aa' 'k' 2 ways
'111' -> 'aaa', 'ka', 'ak'
'1 1 1' '11 1' '1 11'

MAP = {...}

'1123'
'100' -> 0
'1 0 0' '10 0' '1 00' '100'
'01'

'101' -> 'ja'
'10 1'


 - Explictly does not work with uppercase characters.
"""
import unittest
import logging
import string


"""
Implementation
"""

class CipherTranslator(object):

    def __init__(self):
        self.cipher_map = None

    def get_num_cipher_perm(self):
        """

        """
        if not self.s or len(self.s) < 1:
            logging.warning('String not set or empty.')
            return 0

        # Setup map if it does not already exist.
        if not self.cipher_map:
            self.cipher_map = self._get_cipher_map()

        # TODO do real stuff.
        masks = self._get_mask_op_list()
        print ''
        for m in masks:
            print self.mask_to_str(m)
        return len(masks)

    def _get_cipher_map(self):
        alphabet = string.ascii_lowercase
        map = {}
        # '1' = 'a'
        # '2' = 'b'
        # ...
        # '26' = z
        for i in range(len(alphabet)):
            map[str(i + 1)] = alphabet[i]
        return map

    def _get_mask_op_list(self):
        masks = set()
        max_bit = len(self.s) - 1
        max_num = 0
        for i in range(max_bit):
            max_num = max_num + (1 << i)

        for num in range(max_num):
            if self._validate_op_mask(num):
                masks.add(num)

        return masks

    def _validate_op_mask(self, mask):
        bits = self.get_bits(mask)
        for i, b in enumerate(bits):
            if i > 0 and b & bits[i - 1] == 1:
                return False

        return True

    # Partially from http://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
    def get_bits(self, mask):
        bit_list = []
        bit = 1
        while mask >= bit:
            if mask & bit:
                bit_list.append(1)
            else:
                bit_list.append(0)
            bit <<= 1

        return bit_list

    def mask_to_str(self, mask):
        return '{0}: {1}'.format(bin(mask).replace('0b', '')[::-1], mask)

"""
    def _get_mask_op_list(self):
        # TODO: Explain dis yo
        all_masks = set()
        # Track identity masks seperately for dives down permutation tree.
        indentity_masks = []

        for i in range(len(self.s) - 1):
            # Add zero and indentity rows.
            entry = 1 << i
            indentity_masks.append(entry)

            # Find all other masks.
            masks_to_combine = set([entry])
            masks_to_combine = self._find_other_masks(i, indentity_masks, masks_to_combine)

            # Combine to master list.
            all_masks = all_masks.union(masks_to_combine)

        # Add zero mask.
        all_masks.add(0)

        print ''
        for m in all_masks:
            self.print_mask(m)
        return all_masks

    def _find_other_masks(self, start_idx, indentity_masks, masks_to_combine):
        # Check if we can create other combinations.
        # Jump back by 2 recursively.
        back_jump_idx = start_idx - 2
        if back_jump_idx > -1:
            # Combine all current masks for all permutations.
            # TODO: Is there some clever way we can skip combining some of these and wasting cycles?
            masks_to_add = set()
            for mask in masks_to_combine:
                combined_mask = indentity_masks[start_idx] | mask
                if combined_mask == 12:
                    print 'aha ' + str(mask)
                masks_to_add.add(combined_mask)
            masks_to_combine = masks_to_combine.union(masks_to_add)

            # Add the new mask entry.
            new_mask = indentity_masks[start_idx] | indentity_masks[back_jump_idx]
            masks_to_combine.add(new_mask)

            # Continue searching.
            return self._find_other_masks(back_jump_idx, indentity_masks, masks_to_combine)
        else:
            return masks_to_combine

    def _create_permutation_sets(self, s):
        perm_set = set()

        list_s = list(s)
        for i in range(len(list_s)):
            for j in  range(len(list_s)):

                translated_s = ''
                error = False
                for c in perm:
                    translated_c = self.cipher_map.get(c)
                    if not translated_s:
                        error = True
                        break
                    translated_s = translated_s + translated_c
                if not error:
                    perm_set.append(translated_s)

"""

"""
Tests
"""


class CipherTranslatorTest(unittest.TestCase):

    def setUp(self):
        self.subject = CipherTranslator()

        # Normally we'd use a parameterized test framework for this.
        self.test_data = [
            # test num, string, expected result
            #[0, None, 0],
            #[1, '', 0],
            #[2, '0', 0],
            # [3, '1', len(set(['a']))],
            [4, '11', len(set(['aa', 'k']))],
            # [5, '111',len(set(['aaa', 'ak', 'ka']))],  # gewd
            # [6, '1111', len(set(['aaaa', 'kk', 'aka', 'kaa', 'aak']))],  # gewd
            # [7, '11111', len(set(['aaaaa', 'akk', 'kak', 'kka', 'aakaa', 'kaaa', 'aaak']))],
            # [8, '111111', len(set(['aaaaaa', 'aaaak', 'kaaaa', 'aakaa', 'kkk', 'aakk', 'kkaa', 'kaak', 'akaaa', 'aaaka', 'akak', 'kaka']))],
            #[9, '100', 0],
            #[10, '001', 0],
            #[12, '101', 0],
            #[12, '110', 1],  # ja
            #[13, '1123', 5] # aabc, alc, aaw, kw, kbc
        ]

    def test_get_largest_int(self):
        """
        Tests that various valid scenarios return the correct value.
        """
        for entry in self.test_data:
            self.subject.s = entry[1]
            result = self.subject.get_num_cipher_perm()
            self.assertEqual(
                entry[2], result,
                "Test {0} failed with result {1}"
                .format(entry[0], result))


if __name__ == '__main__':
    unittest.main()
