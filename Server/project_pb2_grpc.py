# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import project_pb2 as project__pb2


class StreamServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FetchResponse = channel.unary_stream(
                '/protobuf.StreamService/FetchResponse',
                request_serializer=project__pb2.streamRequest.SerializeToString,
                response_deserializer=project__pb2.streamResponse.FromString,
                )


class StreamServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FetchResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StreamServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FetchResponse': grpc.unary_stream_rpc_method_handler(
                    servicer.FetchResponse,
                    request_deserializer=project__pb2.streamRequest.FromString,
                    response_serializer=project__pb2.streamResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'protobuf.StreamService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class StreamService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FetchResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/protobuf.StreamService/FetchResponse',
            project__pb2.streamRequest.SerializeToString,
            project__pb2.streamResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)