"""Dummy DIMSE-C SCPs for use in unit tests"""

import logging
import os
import socket
import time
import threading

from pydicom import read_file
from pydicom.dataset import Dataset
from pydicom.uid import UID, ImplicitVRLittleEndian, JPEG2000Lossless

from pynetdicom import (
    AE,
    VerificationPresentationContexts,
    build_context,
    StoragePresentationContexts
)
from pynetdicom.sop_class import (
    VerificationSOPClass,
    CTImageStorage, MRImageStorage, RTImageStorage,
    PatientRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelFind,
    ModalityWorklistInformationFind,
    PatientStudyOnlyQueryRetrieveInformationModelFind,
    PatientRootQueryRetrieveInformationModelGet,
    StudyRootQueryRetrieveInformationModelGet,
    PatientStudyOnlyQueryRetrieveInformationModelGet,
    PatientRootQueryRetrieveInformationModelMove,
    StudyRootQueryRetrieveInformationModelMove,
    PatientStudyOnlyQueryRetrieveInformationModelMove,
    CompositeInstanceRetrieveWithoutBulkDataGet,
    GeneralRelevantPatientInformationQuery,
    BreastImagingRelevantPatientInformationQuery,
    CardiacRelevantPatientInformationQuery,
    ProductCharacteristicsQueryInformationModelFind,
    SubstanceApprovalQueryInformationModelFind,
    HangingProtocolStorage,
    CompositeInstanceRootRetrieveGet,
    CompositeInstanceRootRetrieveMove,
    HangingProtocolInformationModelGet,
    HangingProtocolInformationModelFind,
    HangingProtocolInformationModelMove,
    DefinedProcedureProtocolInformationModelGet,
    DefinedProcedureProtocolInformationModelFind,
    DefinedProcedureProtocolInformationModelMove,
    ColorPaletteInformationModelGet,
    ColorPaletteInformationModelFind,
    ColorPaletteInformationModelMove,
    GenericImplantTemplateInformationModelGet,
    GenericImplantTemplateInformationModelFind,
    GenericImplantTemplateInformationModelMove,
    ImplantAssemblyTemplateInformationModelGet,
    ImplantAssemblyTemplateInformationModelFind,
    ImplantAssemblyTemplateInformationModelMove,
    ImplantTemplateGroupInformationModelFind,
    ImplantTemplateGroupInformationModelGet,
    ImplantTemplateGroupInformationModelMove,
)
from pynetdicom.status import code_to_category


LOGGER = logging.getLogger('pynetdicom')
LOGGER.setLevel(logging.CRITICAL)
#LOGGER.setLevel(logging.DEBUG)

TEST_DS_DIR = os.path.join(os.path.dirname(__file__), 'dicom_files')
BIG_DATASET = read_file(os.path.join(TEST_DS_DIR, 'RTImageStorage.dcm'))
DATASET = read_file(os.path.join(TEST_DS_DIR, 'CTImageStorage.dcm'))
COMP_DATASET = read_file(os.path.join(TEST_DS_DIR, 'MRImageStorage_JPG2000_Lossless.dcm'))


class DummyBaseSCP(threading.Thread):
    """Base class for the Dummy SCP classes"""
    bad_status = 0x0101
    def __init__(self):
        """Initialise the class"""
        self.ae.on_c_echo = self.on_c_echo
        self.ae.on_c_store = self.on_c_store
        self.ae.on_c_find = self.on_c_find
        self.ae.on_c_get = self.on_c_get
        self.ae.on_c_move = self.on_c_move
        self.ae.on_n_event_report = self.on_n_event_report
        self.ae.on_n_set = self.on_n_set
        self.ae.on_n_get = self.on_n_get
        self.ae.on_n_action = self.on_n_action
        self.ae.on_n_create = self.on_n_create
        self.ae.on_n_delete = self.on_n_delete

        threading.Thread.__init__(self)
        self.daemon = True

        self.delay = 0
        self.send_abort = False
        self.context = None
        self.info = None

        self.send_a_abort = False
        self.send_ap_abort = False

        self.select_timeout = 0

    def run(self):
        """The thread run method"""
        self.ae.start(select_timeout=self.select_timeout)

    def stop(self):
        """Stop the SCP thread"""
        self.ae.stop()

    def abort(self):
        """Abort any associations"""
        for assoc in self.ae.active_associations:
            assoc.abort()

    def release(self):
        """Release any associations"""
        for assoc in self.ae.active_associations:
            assoc.release()

    def on_c_echo(self, context, info):
        """Callback for ae.on_c_echo"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_store(self, ds, context, info):
        """Callback for ae.on_c_store"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_find(self, ds, context, info):
        """Callback for ae.on_c_find"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_cancel_find(self):
        """Callback for ae.on_c_cancel_find"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_get(self, ds, context, info):
        """Callback for ae.on_c_get"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_cancel_get(self):
        """Callback for ae.on_c_cancel_get"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_move(self, ds, move_aet, context, info):
        """Callback for ae.on_c_move"""
        raise RuntimeError("You should not have been able to get here.")

    def on_c_cancel_move(self):
        """Callback for ae.on_c_cancel_move"""
        raise RuntimeError("You should not have been able to get here.")

    def on_n_event_report(self, ds, evt_id, context, info):
        """Callback for ae.on_n_event_report"""
        raise RuntimeError("You should not have been able to get here.")

    def on_n_get(self, attr, context, info):
        """Callback for ae.on_n_get"""
        raise RuntimeError("You should not have been able to get here.")

    def on_n_set(self, ds, context, info):
        """Callback for ae.on_n_set"""
        raise RuntimeError("You should not have been able to get here.")

    def on_n_action(self, ds, context, info):
        """Callback for ae.on_n_action"""
        raise RuntimeError("You should not have been able to get here.")

    def on_n_create(self, ds, context, info):
        """Callback for ae.on_n_create"""
        raise RuntimeError("You should not have been able to get here.")

    def on_n_delete(self, context, info):
        """Callback for ae.on_n_delete"""
        raise RuntimeError("You should not have been able to get here.")

    def dev_handle_connection(self, client_socket):
        # Create a new Association
        assoc = Association(self, MODE_ACCEPTOR, client_socket)
        assoc.acse_timeout = self.acse_timeout
        assoc.dimse_timeout = self.dimse_timeout
        assoc.network_timeout = self.network_timeout

        # Association Acceptor object -> local AE
        assoc.acceptor.maximum_length = self.maximum_pdu_size
        assoc.acceptor.ae_title = self.ae_title
        assoc.acceptor.address = self.address
        assoc.acceptor.port = self.port
        assoc.acceptor.implementation_class_uid = (
            self.implementation_class_uid
        )
        assoc.acceptor.implementation_version_name = (
            self.implementation_version_name
        )
        assoc.acceptor.supported_contexts = deepcopy(
            self.supported_contexts
        )

        # Association Requestor object -> remote AE
        assoc.requestor.address = client_socket.getpeername()[0]
        assoc.requestor.port = client_socket.getpeername()[1]

        assoc.start()
        self.active_associations.append(assoc)


class DummyVerificationSCP(DummyBaseSCP):
    """A threaded dummy verification SCP used for testing"""
    def __init__(self, port=11112):
        self.ae = AE(port=port)
        self.ae.supported_contexts = VerificationPresentationContexts
        self.ae.add_supported_context('1.2.3.4')
        DummyBaseSCP.__init__(self)
        self.status = 0x0000

    def on_c_echo(self, context, info):
        """Callback for ae.on_c_echo

        Parameters
        ----------
        delay : int or float
            Wait `delay` seconds before sending a response
        """
        self.context = context
        self.info = info
        time.sleep(self.delay)

        if self.send_abort:
            self.ae.active_associations[0].abort()

        return self.status


class DummyStorageSCP(DummyBaseSCP):
    """A threaded dummy storage SCP used for testing"""
    def __init__(self, port=11112):
        self.ae = AE(port=port)
        self.ae.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
        self.ae.add_supported_context(StudyRootQueryRetrieveInformationModelMove)
        self.ae.add_supported_context(PatientStudyOnlyQueryRetrieveInformationModelMove)
        self.ae.add_supported_context(CTImageStorage, scp_role=True, scu_role=True)
        self.ae.add_supported_context(RTImageStorage)
        self.ae.add_supported_context(MRImageStorage, [ImplicitVRLittleEndian, JPEG2000Lossless])
        self.ae.add_supported_context(HangingProtocolStorage)

        DummyBaseSCP.__init__(self)
        self.status = 0x0000
        self.raise_exception = False

    def on_c_store(self, ds, context, info):
        """Callback for ae.on_c_store"""
        self.context = context
        self.info = info
        time.sleep(self.delay)
        if self.raise_exception:
            raise ValueError('Dummy msg')
        return self.status


class DummyFindSCP(DummyBaseSCP):
    """A threaded dummy find SCP used for testing"""
    def __init__(self, port=11112):
        self.ae = AE(port=port)
        self.ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
        self.ae.add_supported_context(StudyRootQueryRetrieveInformationModelFind)
        self.ae.add_supported_context(ModalityWorklistInformationFind)
        self.ae.add_supported_context(PatientStudyOnlyQueryRetrieveInformationModelFind)
        self.ae.add_supported_context(GeneralRelevantPatientInformationQuery)
        self.ae.add_supported_context(BreastImagingRelevantPatientInformationQuery)
        self.ae.add_supported_context(CardiacRelevantPatientInformationQuery)
        self.ae.add_supported_context(ProductCharacteristicsQueryInformationModelFind)
        self.ae.add_supported_context(SubstanceApprovalQueryInformationModelFind)
        self.ae.add_supported_context(HangingProtocolInformationModelFind)
        self.ae.add_supported_context(DefinedProcedureProtocolInformationModelFind)
        self.ae.add_supported_context(ColorPaletteInformationModelFind)
        self.ae.add_supported_context(GenericImplantTemplateInformationModelFind)
        self.ae.add_supported_context(ImplantAssemblyTemplateInformationModelFind)
        self.ae.add_supported_context(ImplantTemplateGroupInformationModelFind)

        DummyBaseSCP.__init__(self)
        self.statuses = [0x0000]
        identifier = Dataset()
        identifier.PatientName = 'Test'
        self.identifiers = [identifier]
        self.cancel = False

    def on_c_find(self, ds, context, info):
        """Callback for ae.on_c_find"""
        self.context = context
        self.info = info
        time.sleep(self.delay)

        for status, identifier in zip(self.statuses, self.identifiers):
            if self.cancel:
                yield 0xFE00, None
                return
            yield status, identifier

    def on_c_cancel_find(self):
        """Callback for ae.on_c_cancel_find"""
        self.cancel = True


class DummyGetSCP(DummyBaseSCP):
    """A threaded dummy get SCP used for testing"""
    def __init__(self, port=11112):
        self.ae = AE(port=port)
        self.ae.add_supported_context(PatientRootQueryRetrieveInformationModelGet)
        self.ae.add_supported_context(StudyRootQueryRetrieveInformationModelGet)
        self.ae.add_supported_context(PatientStudyOnlyQueryRetrieveInformationModelGet)
        self.ae.add_supported_context(CompositeInstanceRetrieveWithoutBulkDataGet)
        self.ae.add_supported_context(CompositeInstanceRootRetrieveGet)
        self.ae.add_supported_context(HangingProtocolInformationModelGet)
        self.ae.add_supported_context(DefinedProcedureProtocolInformationModelGet)
        self.ae.add_supported_context(ColorPaletteInformationModelGet)
        self.ae.add_supported_context(GenericImplantTemplateInformationModelGet)
        self.ae.add_supported_context(ImplantAssemblyTemplateInformationModelGet)
        self.ae.add_supported_context(ImplantTemplateGroupInformationModelGet)
        for cx in StoragePresentationContexts:
            self.ae.add_supported_context(cx.abstract_syntax, scp_role=True, scu_role=False)

        DummyBaseSCP.__init__(self)
        self.statuses = [0x0000]
        ds = Dataset()
        ds.file_meta = Dataset()
        ds.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
        ds.PatientName = 'Test'
        ds.SOPClassUID = CTImageStorage
        ds.SOPInstanceUID = '1.2.3.4'
        self.datasets = [ds]
        self.no_suboperations = 1
        self.cancel = False

    def on_c_get(self, ds, context, info):
        """Callback for ae.on_c_get"""
        self.context = context
        self.info = info
        time.sleep(self.delay)
        ds = Dataset()
        ds.PatientName = '*'
        ds.QueryRetrieveLevel = "PATIENT"

        yield self.no_suboperations
        for (status, ds) in zip(self.statuses, self.datasets):
            if self.cancel:
                yield 0xFE00, None
                return
            yield status, ds

    def on_c_cancel_get(self):
        """Callback for ae.on_c_cancel_get"""
        self.cancel = True


class DummyMoveSCP(DummyBaseSCP):
    """A threaded dummy move SCP used for testing"""
    def __init__(self, port=11112):
        self.ae = AE(port=port)
        self.ae.add_supported_context(PatientRootQueryRetrieveInformationModelMove)
        self.ae.add_supported_context(StudyRootQueryRetrieveInformationModelMove)
        self.ae.add_supported_context(PatientStudyOnlyQueryRetrieveInformationModelMove)
        self.ae.add_supported_context(CompositeInstanceRootRetrieveMove)
        self.ae.add_supported_context(HangingProtocolInformationModelMove)
        self.ae.add_supported_context(DefinedProcedureProtocolInformationModelMove)
        self.ae.add_supported_context(ColorPaletteInformationModelMove)
        self.ae.add_supported_context(GenericImplantTemplateInformationModelMove)
        self.ae.add_supported_context(ImplantAssemblyTemplateInformationModelMove)
        self.ae.add_supported_context(ImplantTemplateGroupInformationModelMove)
        self.ae.add_supported_context(RTImageStorage)
        self.ae.add_supported_context(CTImageStorage)

        self.ae.add_requested_context(RTImageStorage)
        self.ae.add_requested_context(CTImageStorage)

        DummyBaseSCP.__init__(self)
        self.statuses = [0x0000]
        self.store_status = 0x0000
        ds = Dataset()
        ds.file_meta = Dataset()
        ds.file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
        ds.PatientName = 'Test'
        ds.SOPClassUID = CTImageStorage
        ds.SOPInstanceUID = '1.2.3.4'
        self.datasets = [ds]
        self.no_suboperations = 1
        self.destination_ae = ('localhost', 11112)
        self.cancel = False
        self.test_no_yield = False
        self.test_no_subops = False
        self.store_context = None
        self.store_info = None
        self.move_aet = None

    def on_c_move(self, ds, move_aet, context, info):
        """Callback for ae.on_c_move"""
        self.context = context
        self.move_aet = move_aet
        self.info = info
        time.sleep(self.delay)
        ds = Dataset()
        ds.PatientName = '*'
        ds.QueryRetrieveLevel = "PATIENT"

        if self.test_no_yield:
            return

        yield self.destination_ae

        if self.test_no_subops:
            return

        yield self.no_suboperations
        for (status, ds) in zip(self.statuses, self.datasets):
            if self.cancel:
                yield 0xFE00, None
                return
            yield status, ds

    def on_c_store(self, ds, context, info):
        self.store_context = context
        self.store_info = info
        return self.store_status

    def on_c_cancel_move(self):
        """Callback for ae.on_c_cancel_move"""
        self.cancel = True
