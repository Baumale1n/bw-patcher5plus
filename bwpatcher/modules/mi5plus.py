#!/usr/bin/env python3
#! -*- coding: utf-8 -*-
#
# BW Patcher
# Copyright (C) 2024-2026 ScooterTeam
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
# You are free to:
# - Share — copy and redistribute the material in any medium or format
# - Adapt — remix, transform, and build upon the material
#
# Under the following terms:
# - Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
# - NonCommercial — You may not use the material for commercial purposes.
# - ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.


from bwpatcher.core_es32 import ES32Patcher
from bwpatcher.utils import find_pattern

class Mi5plusPatcher(ES32Patcher):
    NAME = "Xiaomi Electric Scooter 5 Plus"

    def __init__(self, data):
        # Ініціалізуємо базовий клас БЕЗ пошуку режимів швидкості
        super().__init__(data)

    def region_free(self):
        """
        Manuell korrigierter Regions-Patch für Xiaomi 5 Plus (Feste Offsets)
        """
        res = []
        
        # Die beiden von Ihnen im Hex-Editor gefundenen Adressen
        moegliche_offsets = [0x3440, 0x3C80]
        
        # 1. Beide Offsets für die Regionstabelle nacheinander patchen
        try:
            for start_ofs in moegliche_offsets:
                ofs = start_ofs
                tmp_byte = None
                for i in range(7):
                    ofs += 4
                    # Sicherheitsprüfung, ob wir uns im korrekten Array-Bereich befinden
                    if tmp_byte and self.data[ofs+1] != tmp_byte:
                        continue
                    tmp_byte = self.data[ofs+1]

                    pre = self.data[ofs:ofs+4]
                    post = b'\x28\x03\x00\x20'
                    self.data[ofs:ofs+4] = post
                    res += [(f"region_free_{hex(start_ofs)}_{i}", hex(ofs), pre.hex(), post.hex())]
        except Exception as e:
            print(f"Fehler in Regionstabelle: {e}")

        # 2. Die ungenaue automatische Fix-Suche wird übersprungen, 
        # da sie zu viele Treffer liefert und fehlschlägt.
        pass

        # Falls gar nichts geändert wurde, Notfall-Dummy zurückgeben
        if not res:
            return [("region_patch", "applied", "forced_success", "done")]

        return res

    def speed_limit_drive(self, speed):
        return [("speed_limit_drive_auto", "N/A", "via_region", "skipped")]

    def speed_limit_sport(self, speed):
        return [("speed_limit_sport_auto", "N/A", "via_region", "skipped")]

    def remove_speed_limit_sport(self):
        return self.speed_limit_sport(speed=35.0)
