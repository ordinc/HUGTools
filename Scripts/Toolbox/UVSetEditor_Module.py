﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import maya.cmds as cmds
from PySide2 import QtWidgets, QtGui, QtCore

# Define minimum window width and height
MIN_WINDOW_WIDTH = 300
MIN_WINDOW_HEIGHT = 400

class RoundedButton(QtWidgets.QPushButton):
    def __init__(self, text):
        super(RoundedButton, self).__init__(text)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #D0D0D0;
                color: #303030;
                border-radius: 10px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
            """
        )

class UVSetEditor_Module_UI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UVSetEditor_Module_UI, self).__init__(parent)
        self.setWindowTitle("UV Set Editor")
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # UV Set List
        self.uv_list = QtWidgets.QListWidget()
        self.uv_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.uv_list.setStyleSheet("""
            QListWidget {
                background-color: #2B2B2B;
                color: #CCCCCC;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #4B4B4B;
            }
            QListWidget::item:hover {
                background-color: #3B3B3B;
            }
        """)

        # Buttons
        self.refresh_btn = RoundedButton("Get")
        self.delete_btn = RoundedButton("Del")
        input_style = """
            QLineEdit {
                background-color: #2B2B2B;
                color: #CCCCCC;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 2px;
            }
        """
        self.new_name_input = QtWidgets.QLineEdit()
        self.new_name_input.setPlaceholderText("Enter a new name or leave it blank")
        self.new_name_input.setStyleSheet(input_style)
        self.create_btn = RoundedButton("New")
        self.rename_btn = RoundedButton("Re")

        # UV Set Swap
        self.uv_set1_input = QtWidgets.QLineEdit()
        self.uv_set1_input.setPlaceholderText("uv1")
        self.uv_set1_input.setStyleSheet(input_style)
        self.uv_set2_input = QtWidgets.QLineEdit()
        self.uv_set2_input.setPlaceholderText("uv2")
        self.uv_set2_input.setStyleSheet(input_style)
        self.get_uv1_btn = RoundedButton("Get")
        self.get_uv2_btn = RoundedButton("Get")
        self.swap_btn = RoundedButton("UV Swap")
        self.reorder_btn = RoundedButton("Reorder Swap")

        # UV Transfer
        self.source_obj_input = QtWidgets.QLineEdit()
        self.source_obj_input.setReadOnly(True)
        self.source_obj_input.setStyleSheet(input_style)
        self.get_source_btn = RoundedButton("Get")
        self.transfer_btn = RoundedButton("Set")

        # Sample Space
        self.sample_space_group = QtWidgets.QButtonGroup(self)
        self.world_radio = QtWidgets.QRadioButton("World")
        self.local_radio = QtWidgets.QRadioButton("Local")
        self.uv_radio = QtWidgets.QRadioButton("UV")
        self.component_radio = QtWidgets.QRadioButton("Component")
        self.sample_space_group.addButton(self.world_radio)
        self.sample_space_group.addButton(self.local_radio)
        self.sample_space_group.addButton(self.uv_radio)
        self.sample_space_group.addButton(self.component_radio)
        self.world_radio.setChecked(True)

        radio_style = """
            QRadioButton {
                color: #CCCCCC;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 13px;
                height: 13px;
            }
            QRadioButton::indicator::unchecked {
                border: 2px solid #555555;
                background-color: #2B2B2B;
                border-radius: 7px;
            }
            QRadioButton::indicator::checked {
                border: 2px solid #555555;
                background-color: #FFFFFF;
                border-radius: 7px;
            }
        """
        self.world_radio.setStyleSheet(radio_style)
        self.local_radio.setStyleSheet(radio_style)
        self.uv_radio.setStyleSheet(radio_style)
        self.component_radio.setStyleSheet(radio_style)

    def create_layouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # UV-Set Frame
        uv_set_frame = QtWidgets.QGroupBox("UV-Set")
        uv_set_layout = QtWidgets.QVBoxLayout(uv_set_frame)
        uv_set_layout.addWidget(self.uv_list)
        uv_set_layout.addWidget(self.new_name_input)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.rename_btn)
        uv_set_layout.addLayout(button_layout)

        # UV-Swap Frame
        uv_swap_frame = QtWidgets.QGroupBox("UV-Swap")
        uv_swap_layout = QtWidgets.QVBoxLayout(uv_swap_frame)
        uv_swap_layout.addWidget(QtWidgets.QLabel("Enter UV set names in \"uv1\" and \"uv2\""))
        uv_swap_layout.addWidget(QtWidgets.QLabel("UV swap or reorder swap."))
        
        uv1_layout = QtWidgets.QHBoxLayout()
        uv1_layout.addWidget(self.get_uv1_btn)
        uv1_layout.addWidget(self.uv_set1_input)
        uv_swap_layout.addLayout(uv1_layout)

        uv2_layout = QtWidgets.QHBoxLayout()
        uv2_layout.addWidget(self.get_uv2_btn)
        uv2_layout.addWidget(self.uv_set2_input)
        uv_swap_layout.addLayout(uv2_layout)
        
        swap_button_layout = QtWidgets.QHBoxLayout()
        swap_button_layout.addWidget(self.swap_btn)
        swap_button_layout.addWidget(self.reorder_btn)
        uv_swap_layout.addLayout(swap_button_layout)

        # UV-Transfer Frame
        uv_transfer_frame = QtWidgets.QGroupBox("UV-Transfer")
        uv_transfer_layout = QtWidgets.QVBoxLayout(uv_transfer_frame)
        
        transfer_input_layout = QtWidgets.QHBoxLayout()
        transfer_input_layout.addWidget(self.get_source_btn)
        transfer_input_layout.addWidget(self.source_obj_input)
        transfer_input_layout.addWidget(self.transfer_btn)
        uv_transfer_layout.addLayout(transfer_input_layout)

        # Sample Space
        sample_space_layout = QtWidgets.QHBoxLayout()
        sample_space_label = QtWidgets.QLabel("Sample Space:")
        sample_space_layout.addWidget(sample_space_label)
        
        sample_space_grid = QtWidgets.QGridLayout()
        sample_space_grid.addWidget(self.world_radio, 0, 0)
        sample_space_grid.addWidget(self.local_radio, 0, 1)
        sample_space_grid.addWidget(self.uv_radio, 1, 0)
        sample_space_grid.addWidget(self.component_radio, 1, 1)
        
        # 使用 QVBoxLayout 来将网格布局放在新的一行
        sample_space_right_layout = QtWidgets.QVBoxLayout()
        sample_space_right_layout.addSpacing(5)  # 添加一些垂直空间
        sample_space_right_layout.addLayout(sample_space_grid)
        
        sample_space_layout.addLayout(sample_space_right_layout)
        uv_transfer_layout.addLayout(sample_space_layout)

        # Add all frames to main layout
        main_layout.addWidget(uv_set_frame)
        main_layout.addWidget(uv_swap_frame)
        main_layout.addWidget(uv_transfer_frame)

    def create_connections(self):
        self.refresh_btn.clicked.connect(self.refresh_uv_sets)
        self.delete_btn.clicked.connect(self.delete_selected_uv_set)
        self.create_btn.clicked.connect(self.create_new_uv_set)
        self.rename_btn.clicked.connect(self.rename_selected_uv_set)
        self.uv_list.itemSelectionChanged.connect(self.switch_uv_set)
        self.swap_btn.clicked.connect(self.UVsetSwap)
        self.reorder_btn.clicked.connect(self.UVsetReorder)
        self.get_source_btn.clicked.connect(self.get_object_name)
        self.transfer_btn.clicked.connect(self.set_uv)
        self.get_uv1_btn.clicked.connect(lambda: self.set_uv_set_name(self.uv_set1_input))
        self.get_uv2_btn.clicked.connect(lambda: self.set_uv_set_name(self.uv_set2_input))

    # Function: Get and display UV sets
    def refresh_uv_sets(self):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning("请先选择一个对象。")
            return

        selected_object = selection[0]
        uv_sets = cmds.polyUVSet(selected_object, query=True, allUVSets=True) or []
        self.uv_list.clear()
        for uv_set in uv_sets:
            self.uv_list.addItem(uv_set)

    # Function: Switch UV set
    def switch_uv_set(self):
        selected_uv_set = self.uv_list.currentItem().text()
        if selected_uv_set:
            selected_object = cmds.ls(selection=True)
            if selected_object:
                selected_object = selected_object[0]
                # Switch current UV set
                cmds.polyUVSet(selected_object, currentUVSet=True, uvSet=selected_uv_set)
                print(f"Switched to UV set: {selected_uv_set}")
            else:
                cmds.warning("Please select an object.")
        else:
            cmds.warning("Please select a UV set.")

    # Function: Delete selected UV set
    def delete_selected_uv_set(self):
        selected_uv_set = self.uv_list.currentItem()
        if selected_uv_set:
            uv_set_name = selected_uv_set.text()
            selected_objects = cmds.ls(selection=True, long=True)
            if not selected_objects:
                cmds.warning("请先选择一个对象。")
                return

            for obj in selected_objects:
                try:
                    if cmds.polyUVSet(obj, query=True, allUVSets=True).count(uv_set_name) > 0:
                        cmds.polyUVSet(obj, delete=True, uvSet=uv_set_name)
                        print(f"已从 {obj} 删除 UV set: {uv_set_name}")
                    else:
                        print(f"{obj} 上不存在 UV set: {uv_set_name}")
                except Exception as e:
                    cmds.warning(f"删除 {obj} 上的 UV set {uv_set_name} 时出错: {str(e)}")

            self.refresh_uv_sets()
        else:
            cmds.warning("请先选择一个 UV set。")

    # Function: Rename selected UV set
    def rename_selected_uv_set(self):
        selected_uv_set = self.uv_list.currentItem()
        new_name = self.new_name_input.text()
        if selected_uv_set and new_name:
            cmds.polyUVSet(rename=True, newUVSet=new_name, uvSet=selected_uv_set.text())
            self.refresh_uv_sets()
            self.new_name_input.clear()  # 清空输入框
        elif not selected_uv_set:
            cmds.warning("请先选择一个 UV set。")
        else:
            cmds.warning("请输入新的名称。")

    # Function: Create new UV set
    def create_new_uv_set(self):
        new_name = self.new_name_input.text().strip()
        selected_objects = cmds.ls(selection=True, long=True)
        
        if not selected_objects:
            cmds.warning("请先选择一个对象。")
            return

        for obj in selected_objects:
            if new_name:
                # 使用用户输入的名称
                uv_set_name = new_name
            else:
                # 自动生成名称（map2, map3, ...）
                existing_uv_sets = cmds.polyUVSet(obj, query=True, allUVSets=True)
                index = 1
                while f"map{index}" in existing_uv_sets:
                    index += 1
                uv_set_name = f"map{index}"

            try:
                cmds.polyUVSet(obj, create=True, uvSet=uv_set_name)
                print(f"在 {obj} 上创建了新的UV set: {uv_set_name}")
            except Exception as e:
                cmds.warning(f"在 {obj} 上创建UV set {uv_set_name} 时出错: {str(e)}")

        self.refresh_uv_sets()
        self.new_name_input.clear()  # 清空输入框

    # Function: UV set swap
    def UVsetSwap(self):
        UVname1 = self.uv_set1_input.text()
        UVname2 = self.uv_set2_input.text()
        selected_objects = cmds.ls(sl=True)
        
        if not selected_objects:
            cmds.warning("请选择一个对象。")
            return

        for obj in selected_objects:
            # 记录操作前的历史节点
            history_before = set(cmds.listHistory(obj))
            
            try:
                cmds.polyUVSet(obj, query=True, allUVSets=True)
                cmds.polyUVSet(obj, create=True, uvSet='TempUV')
                cmds.polyUVSet(obj, copy=True, nuv='TempUV', uvSet=UVname1)
                cmds.polyUVSet(obj, copy=True, nuv=UVname1, uvSet=UVname2)
                cmds.polyUVSet(obj, copy=True, nuv=UVname2, uvSet='TempUV')
                cmds.polyUVSet(obj, delete=True, uvSet='TempUV')
            except Exception as e:
                cmds.warning(f"在 {obj} 上交换 UV set 时出错: {str(e)}")
            
            # 获取操作后的历史节点
            history_after = set(cmds.listHistory(obj))
            
            # 删除新增的历史节点
            new_history = history_after - history_before
            if new_history:
                cmds.delete(list(new_history))
        
        self.refresh_uv_sets()   # 刷新列表
        cmds.select(selected_objects)  # 重新选择对象

    def UVsetReorder(self):
        UVname1 = self.uv_set1_input.text()
        UVname2 = self.uv_set2_input.text()
        print("Reorder object is " + UVname1 + " + " + UVname2)
        
        selected_objects = cmds.ls(sl=True)
        if not selected_objects:
            cmds.warning("请选择一个对象。")
            return

        for obj in selected_objects:
            # 记录操作前的历史节点
            history_before = set(cmds.listHistory(obj))
            
            # 直接使用 polyUVSet 命令进行重排序
            cmds.polyUVSet(obj, reorder=True, uvSet=UVname1, newUVSet=UVname2)

            # 获取操作后的历史节点
            history_after = set(cmds.listHistory(obj))
            
            # 删除新增的历史节点
            new_history = history_after - history_before
            if new_history:
                cmds.delete(list(new_history))

        self.refresh_uv_sets()   # 刷新列表
        cmds.select(selected_objects)  # 重新选择对象

    # Function: UV set transfer
    def get_object_name(self):
        # Get currently selected object and fill its name in the text field
        selected = cmds.ls(sl=True)
        if selected:
            self.source_obj_input.setText(selected[0])
        else:
            cmds.warning("No object selected.")

    def set_uv(self):
        # Get source and target objects, perform UV transfer, and clean up history
        source_object = self.source_obj_input.text()
        target_object = cmds.ls(sl=True)
        if not source_object or not target_object:
            cmds.warning("Please ensure both source and target objects are selected.")
            return
        target_object = target_object[0]
        sample_space_dict = {'World': 0, 'Local': 1, 'UV': 5, 'Component': 4}
        sample_space = self.sample_space_group.checkedId()
        sample_space = sample_space_dict.get(sample_space, 0)
        cmds.transferAttributes(source_object, target_object, transferPositions=0, transferNormals=0, transferUVs=2, transferColors=0, sampleSpace=sample_space, searchMethod=3)
        cmds.delete(target_object, constructionHistory=True)  # Clean up history

    def on_window_resize(self):
        # Check and limit window size
        if self.width() < MIN_WINDOW_WIDTH:
            self.resize(MIN_WINDOW_WIDTH, self.height())
        if self.height() < MIN_WINDOW_HEIGHT:
            self.resize(self.width(), MIN_WINDOW_HEIGHT)

    def set_uv_set_name(self, input_field):
        selected_uv_set = self.uv_list.currentItem()
        if selected_uv_set:
            input_field.setText(selected_uv_set.text())
        else:
            cmds.warning("Please select a UV set first.")

def show():
    global uv_editor_ui
    try:
        uv_editor_ui.close()
        uv_editor_ui.deleteLater()
    except:
        pass
    uv_editor_ui = UVSetEditor_Module_UI()
    uv_editor_ui.show()

if __name__ == "__main__":
    show()
