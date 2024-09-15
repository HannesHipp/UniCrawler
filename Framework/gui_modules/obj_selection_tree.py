from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

from framework.datapoint import Datapoint
from framework.gui_module import GuiModule


class ObjSelectionList(GuiModule):

    def __init__(self, datapoint: Datapoint, tree_view: QTreeView, name_attr: str, checked_attr: str, colored_attr: str) -> None:
        tree_view.setModel(QStandardItemModel())
        tree_view.model.itemChanged.connect(self.update_checkboxes)
        tree_view.setHeaderHidden(True) 
        super().__init__(
            datapoint=datapoint,
            changed_signal=tree_view.model().dataChanged
        )
        self.tree_view = tree_view
        self.name_attr = name_attr
        self.checked_attr = checked_attr
        self.colored_attr = colored_attr

    def get_value(self):
        model = self.tree_view.model()
        result = []
        for i in range(model.rowCount()):
            item = model.item(i)
            object = item.data()
            if item.checkState() == Qt.Checked:
                setattr(object, self.checked_attr, True)
            else:
                setattr(object, self.checked_attr, False)
            result.append(object)
        return result

    def set_value(self, value):
        model = self.tree_view.model()
        if model.rowCount() > 0: 
            return
        model = self.tree_view.model()
        for object in value:
            item = QStandardItem(getattr(object, self.name_attr))
            item.setData(object)
            item.setCheckable(True)
            item.setEditable(False)
            item.setCheckState(Qt.Unchecked)
            if getattr(object, self.checked_attr):
                item.setCheckState(Qt.Checked)
            if getattr(object, self.colored_attr):
                item.setBackground(QBrush(QColor(113, 217, 140)))
                model.insertRow(0, item)
            else:
                model.appendRow(item)


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