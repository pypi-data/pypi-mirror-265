# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.identity.v2 import job_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2


class JobStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.delete = channel.unary_unary(
                '/spaceone.api.identity.v2.Job/delete',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v2.Job/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.identity.v2.Job/list',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobsQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.identity.v2.Job/stat',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class JobServicer(object):
    """Missing associated documentation comment in .proto file."""

    def delete(self, request, context):
        """Deletes a specific Job. You must specify the `job_id` of the Job to delete.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Gets a specific Job. Prints detailed information about the Job, including its state.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of all Jobs. You can use a query to get a filtered list of Jobs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JobServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobsQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v2.Job', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Job(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.Job/delete',
            spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.Job/get',
            spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.Job/list',
            spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobsQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.Job/stat',
            spaceone_dot_api_dot_identity_dot_v2_dot_job__pb2.JobStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
