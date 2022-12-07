"""
Windows need install pywin32 python module first.
pip install pywin32
"""

import random
import time
import win32api
from win32con import *

class PyKeyboardMeta(object):
    
    def tap_key(self, character='', n=5, interval=5):
        """press and release a given character key n times"""
        for i in range(n):
            self.press_key(character)
            self.release_key(character)
            time.sleep(interval)
    
    def special_key_assignment(self):
        raise NotImplementedError
    
    def press_keys(self,characters=[]):
        """Press a given character key."""
        for character in characters:
            self.press_key(character)
        for character in characters:
            self.release_key(character)
    
    def is_char_shifted(self, character):
        """Returns True if the key character is uppercase or shifted."""
        if character.isupper():
            return True
        if character in '<>?:"{}|~!@#$%^&*()_+':
            return True
        return False


class PyKeyboard(PyKeyboardMeta):
    def __init__(self):
        PyKeyboardMeta.__init__(self)
        self.special_key_assignment()
    
    def press_key(self, character=''):
        try:
            shifted = self.is_char_shifted(character)
        except AttributeError:
            win32api.keybd_event(character, 0, 0, 0)
        else:
            if shifted:
                win32api.keybd_event(self.shift_key, 0, 0, 0)
            char_vk = win32api.VkKeyScan(character)
            win32api.keybd_event(char_vk, 0, 0, 0)
    
    def release_key(self, character=''):
        try:
            shifted = self.is_char_shifted(character)
        except AttributeError:
            win32api.keybd_event(character, 0, KEYEVENTF_KEYUP, 0)
        else:
            if shifted:
                win32api.keybd_event(self.shift_key, 0, KEYEVENTF_KEYUP, 0)
            char_vk = win32api.VkKeyScan(character)
            win32api.keybd_event(char_vk, 0, KEYEVENTF_KEYUP, 0)
    
    def special_key_assignment(self):
        self.backspace_key = VK_BACK
        self.tab_key = VK_TAB
        self.clear_key = VK_CLEAR
        self.return_key = VK_RETURN
        self.enter_key = self.return_key  # Because many keyboards call it "Enter"
        self.shift_key = VK_SHIFT
        self.shift_l_key = VK_LSHIFT
        self.shift_r_key = VK_RSHIFT
        self.control_key = VK_CONTROL
        self.control_l_key = VK_LCONTROL
        self.control_r_key = VK_RCONTROL
        #Windows uses "menu" to refer to Alt...
        self.menu_key = VK_MENU
        self.alt_l_key = VK_LMENU
        self.alt_r_key = VK_RMENU
        self.altgr_key = VK_RMENU
        self.alt_key = self.alt_l_key
        self.pause_key = VK_PAUSE
        self.caps_lock_key = VK_CAPITAL
        self.capital_key = self.caps_lock_key
        self.num_lock_key = VK_NUMLOCK
        self.scroll_lock_key = VK_SCROLL
        #Windows Language Keys,
        self.kana_key = VK_KANA
        self.hangeul_key = VK_HANGEUL # old name - should be here for compatibility
        self.hangul_key = VK_HANGUL
        self.junjua_key = VK_JUNJA
        self.final_key = VK_FINAL
        self.hanja_key = VK_HANJA
        self.kanji_key = VK_KANJI
        self.convert_key = VK_CONVERT
        self.nonconvert_key = VK_NONCONVERT
        self.accept_key = VK_ACCEPT
        self.modechange_key = VK_MODECHANGE
        #More Keys
        self.escape_key = VK_ESCAPE
        self.space_key = VK_SPACE
        self.prior_key = VK_PRIOR
        self.next_key = VK_NEXT
        self.page_up_key = self.prior_key
        self.page_down_key = self.next_key
        self.home_key = VK_HOME
        self.up_key = VK_UP
        self.down_key = VK_DOWN
        self.left_key = VK_LEFT
        self.right_key = VK_RIGHT
        self.end_key = VK_END
        self.select_key = VK_SELECT
        self.print_key = VK_PRINT
        self.snapshot_key = VK_SNAPSHOT
        self.print_screen_key = self.snapshot_key
        self.execute_key = VK_EXECUTE
        self.insert_key = VK_INSERT
        self.delete_key = VK_DELETE
        self.help_key = VK_HELP
        self.windows_l_key = VK_LWIN
        self.super_l_key = self.windows_l_key
        self.windows_r_key = VK_RWIN
        self.super_r_key = self.windows_r_key
        self.apps_key = VK_APPS
        #Numpad
        self.keypad_keys = {'Space': None,
                            'Tab': None,
                            'Enter': None,  # Needs Fixing
                            'F1': None,
                            'F2': None,
                            'F3': None,
                            'F4': None,
                            'Home': VK_NUMPAD7,
                            'Left': VK_NUMPAD4,
                            'Up': VK_NUMPAD8,
                            'Right': VK_NUMPAD6,
                            'Down': VK_NUMPAD2,
                            'Prior': None,
                            'Page_Up': VK_NUMPAD9,
                            'Next': None,
                            'Page_Down': VK_NUMPAD3,
                            'End': VK_NUMPAD1,
                            'Begin': None,
                            'Insert': VK_NUMPAD0,
                            'Delete': VK_DECIMAL,
                            'Equal': None,  # Needs Fixing
                            'Multiply': VK_MULTIPLY,
                            'Add': VK_ADD,
                            'Separator': VK_SEPARATOR,
                            'Subtract': VK_SUBTRACT,
                            'Decimal': VK_DECIMAL,
                            'Divide': VK_DIVIDE,
                            0: VK_NUMPAD0,
                            1: VK_NUMPAD1,
                            2: VK_NUMPAD2,
                            3: VK_NUMPAD3,
                            4: VK_NUMPAD4,
                            5: VK_NUMPAD5,
                            6: VK_NUMPAD6,
                            7: VK_NUMPAD7,
                            8: VK_NUMPAD8,
                            9: VK_NUMPAD9}
        self.numpad_keys = self.keypad_keys
        #FKeys
        self.function_keys = [None, VK_F1, VK_F2, VK_F3, VK_F4, VK_F5, VK_F6,
                              VK_F7, VK_F8, VK_F9, VK_F10, VK_F11, VK_F12,
                              VK_F13, VK_F14, VK_F15, VK_F16, VK_F17, VK_F18,
                              VK_F19, VK_F20, VK_F21, VK_F22, VK_F23, VK_F24,
                              None, None, None, None, None, None, None, None,
                              None, None, None]  # Up to 36 as in x11
        #Miscellaneous
        self.cancel_key = VK_CANCEL
        self.break_key = self.cancel_key
        self.mode_switch_key = VK_MODECHANGE
        self.browser_back_key = VK_BROWSER_BACK
        self.browser_forward_key = VK_BROWSER_FORWARD
        self.processkey_key = VK_PROCESSKEY
        self.attn_key = VK_ATTN
        self.crsel_key = VK_CRSEL
        self.exsel_key = VK_EXSEL
        self.ereof_key = VK_EREOF
        self.play_key = VK_PLAY
        self.zoom_key = VK_ZOOM
        self.noname_key = VK_NONAME
        self.pa1_key = VK_PA1
        self.oem_clear_key = VK_OEM_CLEAR
        self.volume_mute_key = VK_VOLUME_MUTE
        self.volume_down_key = VK_VOLUME_DOWN
        self.volume_up_key = VK_VOLUME_UP
        self.media_next_track_key = VK_MEDIA_NEXT_TRACK
        self.media_prev_track_key = VK_MEDIA_PREV_TRACK
        self.media_play_pause_key = VK_MEDIA_PLAY_PAUSE
        self.begin_key = self.home_key
        #LKeys - Unsupported
        self.l_keys = [None] * 11
        #RKeys - Unsupported
        self.r_keys = [None] * 16

        #Other unsupported Keys from X11
        self.linefeed_key = None
        self.find_key = None
        self.meta_l_key = None
        self.meta_r_key = None
        self.sys_req_key = None
        self.hyper_l_key = None
        self.hyper_r_key = None
        self.undo_key = None
        self.redo_key = None
        self.script_switch_key = None


if __name__ == "__main__":
    k = PyKeyboard()
    # k.tap_key(k.windows_l_key)
    # interval = 4
    while 1:
        rani = str(random.randint(4,6))
        print("current window is %s\n" % rani)
        k.press_keys([k.windows_l_key, rani])
        time.sleep(random.randint(5,10))
        print("back to desktop\n")
        k.press_keys([k.windows_l_key, 'd'])
        time.sleep(180)
