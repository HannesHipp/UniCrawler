from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

from framework.datapoint import Datapoint
from framework.gui_module import GuiModule


class ObjSelectionTree(GuiModule):

    def __init__(self, 
                 datapoint: Datapoint, 
                 tree_view: QTreeView, 
                 name_attr: str, 
                 checked_attr: str, 
                 colored_attr: str,
                 parent_attr: str) -> None:
        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self.update_checkboxes)
        tree_view.setModel(self.model)
        tree_view.setHeaderHidden(True) 
        super().__init__(
            datapoint=datapoint,
            changed_signal=self.model.dataChanged
        )
        self.tree_view = tree_view
        self.name_attr = name_attr
        self.checked_attr = checked_attr
        self.colored_attr = colored_attr
        self.parent_attr = parent_attr

    def get_value(self):
        result = []
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            object = item.data()
            if item.checkState() == Qt.Checked:
                setattr(object, self.checked_attr, True)
            else:
                setattr(object, self.checked_attr, False)
            result.append(object)
        return result

    def set_value(self, value):
        if self.model.rowCount() > 0: 
            return
        parents = {}
        for object in value:
            parent_object = getattr(object, self.parent_attr)
            if parent_object not in parents:
                parent_item = QStandardItem(getattr(parent_object, self.name_attr))
                parent_item.setData(parent_object)
                parent_item.setCheckable(True)
                parent_item.setEditable(False)
                parent_item.setCheckState(Qt.Unchecked)
                self.model.appendRow(parent_item)
                parents[parent_object] = parent_item
            
            parent_item = parents[parent_object]
            item = QStandardItem(getattr(object, self.name_attr))
            item.setData(object)
            item.setCheckable(True)
            item.setEditable(False)
            item.setCheckState(Qt.Unchecked)
            if getattr(object, self.checked_attr):
                item.setCheckState(Qt.Checked)
            if getattr(object, self.colored_attr):
                item.setBackground(QBrush(QColor(113, 217, 140)))
                parent_item.insertRow(0, item)
            else:
                parent_item.appendRow(item)
            self.update_checkboxes(item)


    def update_checkboxes(self, item):
        if not item.isCheckable() or self.model.blockSignals(True): 
            return 

        state = item.checkState()
        if not item.parent(): 
            for row in range(item.rowCount()):
                child = item.child(row)
                child.setCheckState(state)
        else: 
            parent = item.parent()
            all_checked = all(parent.child(i).checkState() == Qt.Checked 
                              for i in range(parent.rowCount()))
            parent.setCheckState(Qt.Checked if all_checked else Qt.Unchecked)

        self.model.blockSignals(False) 

        self.model.dataChanged.emit(QModelIndex(), QModelIndex()) 