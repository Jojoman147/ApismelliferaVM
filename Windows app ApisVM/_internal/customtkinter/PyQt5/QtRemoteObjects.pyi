# The PEP 484 type hints stub file for the QtRemoteObjects module.
#
# Generated by SIP 6.8.6
#
# Copyright (c) 2024 Riverbank Computing Limited <info@riverbankcomputing.com>
# 
# This file is part of PyQt5.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


import typing

import PyQt5.sip

from PyQt5 import QtCore

# Support for QDate, QDateTime and QTime.
import datetime

# Convenient type aliases.
PYQT_SIGNAL = typing.Union[QtCore.pyqtSignal, QtCore.pyqtBoundSignal]
PYQT_SLOT = typing.Union[typing.Callable[..., Any], QtCore.pyqtBoundSignal]


class QAbstractItemModelReplica(QtCore.QAbstractItemModel):

    initialized: typing.ClassVar[QtCore.pyqtSignal]
    def setRootCacheSize(self, rootCacheSize: int) -> None: ...
    def rootCacheSize(self) -> int: ...
    def hasData(self, index: QtCore.QModelIndex, role: int) -> bool: ...
    def isInitialized(self) -> bool: ...
    def roleNames(self) -> typing.Dict[int, QtCore.QByteArray]: ...
    def availableRoles(self) -> typing.List[int]: ...
    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags: ...
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int) -> typing.Any: ...
    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int: ...
    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int: ...
    def hasChildren(self, parent: QtCore.QModelIndex = ...) -> bool: ...
    def index(self, row: int, column: int, parent: QtCore.QModelIndex = ...) -> QtCore.QModelIndex: ...
    def parent(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex: ...
    def setData(self, index: QtCore.QModelIndex, value: typing.Any, role: int = ...) -> bool: ...
    def data(self, index: QtCore.QModelIndex, role: int = ...) -> typing.Any: ...
    def selectionModel(self) -> typing.Optional[QtCore.QItemSelectionModel]: ...


class QRemoteObjectReplica(QtCore.QObject):

    class State(int):
        Uninitialized = ... # type: QRemoteObjectReplica.State
        Default = ... # type: QRemoteObjectReplica.State
        Valid = ... # type: QRemoteObjectReplica.State
        Suspect = ... # type: QRemoteObjectReplica.State
        SignatureMismatch = ... # type: QRemoteObjectReplica.State

    notified: typing.ClassVar[QtCore.pyqtSignal]
    stateChanged: typing.ClassVar[QtCore.pyqtSignal]
    initialized: typing.ClassVar[QtCore.pyqtSignal]
    def setNode(self, node: typing.Optional['QRemoteObjectNode']) -> None: ...
    def node(self) -> typing.Optional['QRemoteObjectNode']: ...
    def state(self) -> 'QRemoteObjectReplica.State': ...
    def isInitialized(self) -> bool: ...
    def waitForSource(self, timeout: int = ...) -> bool: ...
    def isReplicaValid(self) -> bool: ...


class QRemoteObjectDynamicReplica(QRemoteObjectReplica): ...


class QRemoteObjectAbstractPersistedStore(QtCore.QObject):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def restoreProperties(self, repName: typing.Optional[str], repSig: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> typing.List[typing.Any]: ...
    def saveProperties(self, repName: typing.Optional[str], repSig: typing.Union[QtCore.QByteArray, bytes, bytearray], values: typing.Iterable[typing.Any]) -> None: ...


class QRemoteObjectNode(QtCore.QObject):

    class ErrorCode(int):
        NoError = ... # type: QRemoteObjectNode.ErrorCode
        RegistryNotAcquired = ... # type: QRemoteObjectNode.ErrorCode
        RegistryAlreadyHosted = ... # type: QRemoteObjectNode.ErrorCode
        NodeIsNoServer = ... # type: QRemoteObjectNode.ErrorCode
        ServerAlreadyCreated = ... # type: QRemoteObjectNode.ErrorCode
        UnintendedRegistryHosting = ... # type: QRemoteObjectNode.ErrorCode
        OperationNotValidOnClientNode = ... # type: QRemoteObjectNode.ErrorCode
        SourceNotRegistered = ... # type: QRemoteObjectNode.ErrorCode
        MissingObjectName = ... # type: QRemoteObjectNode.ErrorCode
        HostUrlInvalid = ... # type: QRemoteObjectNode.ErrorCode
        ProtocolMismatch = ... # type: QRemoteObjectNode.ErrorCode
        ListenFailed = ... # type: QRemoteObjectNode.ErrorCode

    @typing.overload
    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, registryAddress: QtCore.QUrl, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def timerEvent(self, a0: typing.Optional[QtCore.QTimerEvent]) -> None: ...
    heartbeatIntervalChanged: typing.ClassVar[QtCore.pyqtSignal]
    error: typing.ClassVar[QtCore.pyqtSignal]
    remoteObjectRemoved: typing.ClassVar[QtCore.pyqtSignal]
    remoteObjectAdded: typing.ClassVar[QtCore.pyqtSignal]
    def setHeartbeatInterval(self, interval: int) -> None: ...
    def heartbeatInterval(self) -> int: ...
    def lastError(self) -> 'QRemoteObjectNode.ErrorCode': ...
    def setPersistedStore(self, persistedStore: typing.Optional[QRemoteObjectAbstractPersistedStore]) -> None: ...
    def persistedStore(self) -> typing.Optional[QRemoteObjectAbstractPersistedStore]: ...
    def registry(self) -> typing.Optional['QRemoteObjectRegistry']: ...
    def waitForRegistry(self, timeout: int = ...) -> bool: ...
    def setRegistryUrl(self, registryAddress: QtCore.QUrl) -> bool: ...
    def registryUrl(self) -> QtCore.QUrl: ...
    def acquireModel(self, name: typing.Optional[str], action: 'QtRemoteObjects.InitialAction' = ..., rolesHint: typing.Iterable[int] = ...) -> typing.Optional[QAbstractItemModelReplica]: ...
    def acquireDynamic(self, name: typing.Optional[str]) -> typing.Optional[QRemoteObjectDynamicReplica]: ...
    def instances(self, typeName: typing.Optional[str]) -> typing.List[str]: ...
    def setName(self, name: typing.Optional[str]) -> None: ...
    def addClientSideConnection(self, ioDevice: typing.Optional[QtCore.QIODevice]) -> None: ...
    def connectToNode(self, address: QtCore.QUrl) -> bool: ...


class QRemoteObjectHostBase(QRemoteObjectNode):

    class AllowedSchemas(int):
        BuiltInSchemasOnly = ... # type: QRemoteObjectHostBase.AllowedSchemas
        AllowExternalRegistration = ... # type: QRemoteObjectHostBase.AllowedSchemas

    def reverseProxy(self) -> bool: ...
    def proxy(self, registryUrl: QtCore.QUrl, hostUrl: QtCore.QUrl = ...) -> bool: ...
    def addHostSideConnection(self, ioDevice: typing.Optional[QtCore.QIODevice]) -> None: ...
    def disableRemoting(self, remoteObject: typing.Optional[QtCore.QObject]) -> bool: ...
    @typing.overload
    def enableRemoting(self, object: typing.Optional[QtCore.QObject], name: typing.Optional[str] = ...) -> bool: ...
    @typing.overload
    def enableRemoting(self, model: typing.Optional[QtCore.QAbstractItemModel], name: typing.Optional[str], roles: typing.Iterable[int], selectionModel: typing.Optional[QtCore.QItemSelectionModel] = ...) -> bool: ...
    def setName(self, name: typing.Optional[str]) -> None: ...


class QRemoteObjectHost(QRemoteObjectHostBase):

    @typing.overload
    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, address: QtCore.QUrl, registryAddress: QtCore.QUrl = ..., allowedSchemas: QRemoteObjectHostBase.AllowedSchemas = ..., parent: typing.Optional[QtCore.QObject] = ...) -> None: ...
    @typing.overload
    def __init__(self, address: QtCore.QUrl, parent: typing.Optional[QtCore.QObject]) -> None: ...

    hostUrlChanged: typing.ClassVar[QtCore.pyqtSignal]
    def setHostUrl(self, hostAddress: QtCore.QUrl, allowedSchemas: QRemoteObjectHostBase.AllowedSchemas = ...) -> bool: ...
    def hostUrl(self) -> QtCore.QUrl: ...


class QRemoteObjectRegistryHost(QRemoteObjectHostBase):

    def __init__(self, registryAddress: QtCore.QUrl = ..., parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def setRegistryUrl(self, registryUrl: QtCore.QUrl) -> bool: ...


class QRemoteObjectRegistry(QRemoteObjectReplica):

    remoteObjectRemoved: typing.ClassVar[QtCore.pyqtSignal]
    remoteObjectAdded: typing.ClassVar[QtCore.pyqtSignal]
    def sourceLocations(self) -> typing.Dict[str, 'QRemoteObjectSourceLocationInfo']: ...


class QRemoteObjectSourceLocationInfo(PyQt5.sipsimplewrapper):

    hostUrl = ... # type: QtCore.QUrl
    typeName = ... # type: typing.Optional[str]

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, typeName_: typing.Optional[str], hostUrl_: QtCore.QUrl) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QRemoteObjectSourceLocationInfo') -> None: ...

    def __ne__(self, other: object): ...
    def __eq__(self, other: object): ...


class QtRemoteObjects(PyQt5.sip.simplewrapper):

    class InitialAction(int):
        FetchRootSize = ... # type: QtRemoteObjects.InitialAction
        PrefetchData = ... # type: QtRemoteObjects.InitialAction
