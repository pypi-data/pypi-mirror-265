# This program source code file is part of KiCad, a free EDA CAD application.
#
# Copyright (C) 2024 KiCad Developers
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# THIS FILE WAS GENERATED AUTOMATICALLY - DO NOT EDIT

from enum import Enum, unique

@unique
class PCB_LAYER_ID(Enum):
    """KiCad's PCB_LAYER_ID enum type"""
    UNSELECTED_LAYER = -2
    UNDEFINED_LAYER = -1
    F_Cu = 0
    In1_Cu = 1
    In2_Cu = 2
    In3_Cu = 3
    In4_Cu = 4
    In5_Cu = 5
    In6_Cu = 6
    In7_Cu = 7
    In8_Cu = 8
    In9_Cu = 9
    In10_Cu = 10
    In11_Cu = 11
    In12_Cu = 12
    In13_Cu = 13
    In14_Cu = 14
    In15_Cu = 15
    In16_Cu = 16
    In17_Cu = 17
    In18_Cu = 18
    In19_Cu = 19
    In20_Cu = 20
    In21_Cu = 21
    In22_Cu = 22
    In23_Cu = 23
    In24_Cu = 24
    In25_Cu = 25
    In26_Cu = 26
    In27_Cu = 27
    In28_Cu = 28
    In29_Cu = 29
    In30_Cu = 30
    B_Cu = 31
    B_Adhes = 32
    F_Adhes = 33
    B_Paste = 34
    F_Paste = 35
    B_SilkS = 36
    F_SilkS = 37
    B_Mask = 38
    F_Mask = 39
    Dwgs_User = 40
    Cmts_User = 41
    Eco1_User = 42
    Eco2_User = 43
    Edge_Cuts = 44
    Margin = 45
    B_CrtYd = 46
    F_CrtYd = 47
    B_Fab = 48
    F_Fab = 49
    User_1 = 50
    User_2 = 51
    User_3 = 52
    User_4 = 53
    User_5 = 54
    User_6 = 55
    User_7 = 56
    User_8 = 57
    User_9 = 58
    Rescue = 59
    PCB_LAYER_ID_COUNT = 60
            
class SHAPE_T(Enum):
    """KiCad's SHAPE_T enum type"""
    UNDEFINED = -1
    SEGMENT = 0
    RECTANGLE = 1
    ARC = 2
    CIRCLE = 3
    POLY = 4
    BEZIER = 5
            
class KICAD_T(Enum):
    """KiCad's KICAD_T enum type"""
    NOT_USED = -1
    TYPE_NOT_INIT = 0
    PCB_T = 1
    SCREEN_T = 2
    PCB_FOOTPRINT_T = 3
    PCB_PAD_T = 4
    PCB_SHAPE_T = 5
    PCB_REFERENCE_IMAGE_T = 6
    PCB_FIELD_T = 7
    PCB_GENERATOR_T = 8
    PCB_TEXT_T = 9
    PCB_TEXTBOX_T = 10
    PCB_TABLE_T = 11
    PCB_TABLECELL_T = 12
    PCB_TRACE_T = 13
    PCB_VIA_T = 14
    PCB_ARC_T = 15
    PCB_MARKER_T = 16
    PCB_DIMENSION_T = 17
    PCB_DIM_ALIGNED_T = 18
    PCB_DIM_LEADER_T = 19
    PCB_DIM_CENTER_T = 20
    PCB_DIM_RADIAL_T = 21
    PCB_DIM_ORTHOGONAL_T = 22
    PCB_TARGET_T = 23
    PCB_ZONE_T = 24
    PCB_ITEM_LIST_T = 25
    PCB_NETINFO_T = 26
    PCB_GROUP_T = 27
    PCB_FIELD_LOCATE_REFERENCE_T = 28
    PCB_FIELD_LOCATE_VALUE_T = 29
    PCB_FIELD_LOCATE_FOOTPRINT_T = 30
    PCB_FIELD_LOCATE_DATASHEET_T = 31
    PCB_LOCATE_STDVIA_T = 32
    PCB_LOCATE_UVIA_T = 33
    PCB_LOCATE_BBVIA_T = 34
    PCB_LOCATE_TEXT_T = 35
    PCB_LOCATE_HOLE_T = 36
    PCB_LOCATE_PTH_T = 37
    PCB_LOCATE_NPTH_T = 38
    PCB_LOCATE_BOARD_EDGE_T = 39
    PCB_SHAPE_LOCATE_SEGMENT_T = 40
    PCB_SHAPE_LOCATE_RECT_T = 41
    PCB_SHAPE_LOCATE_CIRCLE_T = 42
    PCB_SHAPE_LOCATE_ARC_T = 43
    PCB_SHAPE_LOCATE_POLY_T = 44
    PCB_SHAPE_LOCATE_BEZIER_T = 45
    SCH_MARKER_T = 46
    SCH_JUNCTION_T = 47
    SCH_NO_CONNECT_T = 48
    SCH_BUS_WIRE_ENTRY_T = 49
    SCH_BUS_BUS_ENTRY_T = 50
    SCH_LINE_T = 51
    SCH_SHAPE_T = 52
    SCH_BITMAP_T = 53
    SCH_TEXTBOX_T = 54
    SCH_TEXT_T = 55
    SCH_TABLE_T = 56
    SCH_TABLECELL_T = 57
    SCH_LABEL_T = 58
    SCH_GLOBAL_LABEL_T = 59
    SCH_HIER_LABEL_T = 60
    SCH_DIRECTIVE_LABEL_T = 61
    SCH_FIELD_T = 62
    SCH_SYMBOL_T = 63
    SCH_SHEET_PIN_T = 64
    SCH_SHEET_T = 65
    SCH_PIN_T = 66
    SCH_FIELD_LOCATE_REFERENCE_T = 67
    SCH_FIELD_LOCATE_VALUE_T = 68
    SCH_FIELD_LOCATE_FOOTPRINT_T = 69
    SCH_FIELD_LOCATE_DATASHEET_T = 70
    SCH_ITEM_LOCATE_WIRE_T = 71
    SCH_ITEM_LOCATE_BUS_T = 72
    SCH_ITEM_LOCATE_GRAPHIC_LINE_T = 73
    SCH_LABEL_LOCATE_ANY_T = 74
    SCH_LABEL_LOCATE_WIRE_T = 75
    SCH_LABEL_LOCATE_BUS_T = 76
    SCH_SYMBOL_LOCATE_POWER_T = 77
    SCH_LOCATE_ANY_T = 78
    SCH_SCREEN_T = 79
    SCHEMATIC_T = 80
    LIB_SYMBOL_T = 81
    LIB_SHAPE_T = 82
    LIB_TEXT_T = 83
    LIB_TEXTBOX_T = 84
    LIB_PIN_T = 85
    LIB_FIELD_T = 86
    GERBER_LAYOUT_T = 87
    GERBER_DRAW_ITEM_T = 88
    GERBER_IMAGE_T = 89
    WSG_LINE_T = 90
    WSG_RECT_T = 91
    WSG_POLY_T = 92
    WSG_TEXT_T = 93
    WSG_BITMAP_T = 94
    WSG_PAGE_T = 95
    WS_PROXY_UNDO_ITEM_T = 96
    WS_PROXY_UNDO_ITEM_PLUS_T = 97
    SYMBOL_LIB_TABLE_T = 98
    FP_LIB_TABLE_T = 99
    SYMBOL_LIBS_T = 100
    SEARCH_STACK_T = 101
    S3D_CACHE_T = 102
    MAX_STRUCT_TYPE_ID = 103
            
