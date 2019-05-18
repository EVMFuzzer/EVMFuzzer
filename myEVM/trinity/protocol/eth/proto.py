import logging
from typing import (
    List,
    Tuple,
    TYPE_CHECKING,
    Union,
)

from eth_typing import (
    Hash32,
    BlockNumber,
)

from eth.rlp.headers import BlockHeader
from eth.rlp.receipts import Receipt
from eth.rlp.transactions import BaseTransactionFields

from p2p.protocol import (
    Protocol,
)

from trinity.rlp.block_body import BlockBody

from .commands import (
    BlockBodies,
    BlockHeaders,
    GetBlockBodies,
    GetBlockHeaders,
    GetNodeData,
    GetReceipts,
    NewBlock,
    NewBlockHashes,
    NodeData,
    Receipts,
    Status,
    Transactions,
)
from .requests import (
    BlockBodiesRequest,
    HeaderRequest,
    NodeDataRequest,
    ReceiptsRequest,
)

if TYPE_CHECKING:
    from p2p.peer import (  # noqa: F401
        ChainInfo
    )


class ETHProtocol(Protocol):
    name = 'eth'
    version = 63
    _commands = [
        Status, NewBlockHashes, Transactions, GetBlockHeaders, BlockHeaders,
        GetBlockBodies, BlockBodies, NewBlock, GetNodeData, NodeData,
        GetReceipts, Receipts]
    cmd_length = 17
    logger = logging.getLogger("p2p.eth.ETHProtocol")

    def send_handshake(self, head_info: 'ChainInfo') -> None:
        resp = {
            'protocol_version': self.version,
            'network_id': self.peer.network_id,
            'td': head_info.total_difficulty,
            'best_hash': head_info.block_hash,
            'genesis_hash': head_info.genesis_hash,
        }
        cmd = Status(self.cmd_id_offset)
        self.logger.debug("Sending ETH/Status msg: %s", resp)
        self.send(*cmd.encode(resp))

    #
    # Node Data
    #
    def send_get_node_data(self, request: NodeDataRequest) -> None:
        self._send_get_node_data(request.node_hashes)

    def _send_get_node_data(self, node_hashes: Tuple[Hash32, ...]) -> None:
        cmd = GetNodeData(self.cmd_id_offset)
        header, body = cmd.encode(node_hashes)
        self.send(header, body)

    def send_node_data(self, nodes: Tuple[bytes, ...]) -> None:
        cmd = NodeData(self.cmd_id_offset)
        header, body = cmd.encode(nodes)
        self.send(header, body)

    #
    # Block Headers
    #
    def send_get_block_headers(self, request: HeaderRequest) -> None:
        """Send a GetBlockHeaders msg to the remote.

        This requests that the remote send us up to max_headers, starting from
        block_number_or_hash if reverse is False or ending at block_number_or_hash if reverse is
        True.
        """
        self._send_get_block_headers(
            block_number_or_hash=request.block_number_or_hash,
            max_headers=request.max_headers,
            skip=request.skip,
            reverse=request.reverse,
        )

    def _send_get_block_headers(self,
                                block_number_or_hash: Union[BlockNumber, Hash32],
                                max_headers: int,
                                skip: int,
                                reverse: bool) -> None:
        cmd = GetBlockHeaders(self.cmd_id_offset)
        data = {
            'block_number_or_hash': block_number_or_hash,
            'max_headers': max_headers,
            'skip': skip,
            'reverse': reverse
        }
        header, body = cmd.encode(data)
        self.send(header, body)

    def send_block_headers(self, headers: Tuple[BlockHeader, ...]) -> None:
        cmd = BlockHeaders(self.cmd_id_offset)
        header, body = cmd.encode(headers)
        self.send(header, body)

    #
    # Block Bodies
    #
    def send_get_block_bodies(self, request: BlockBodiesRequest) -> None:
        self._send_get_block_bodies(request.block_hashes)

    def _send_get_block_bodies(self, block_hashes: Tuple[Hash32, ...]) -> None:
        cmd = GetBlockBodies(self.cmd_id_offset)
        header, body = cmd.encode(block_hashes)
        self.send(header, body)

    def send_block_bodies(self, blocks: List[BlockBody]) -> None:
        cmd = BlockBodies(self.cmd_id_offset)
        header, body = cmd.encode(blocks)
        self.send(header, body)

    #
    # Receipts
    #
    def send_get_receipts(self, request: ReceiptsRequest) -> None:
        self._send_get_receipts(request.block_hashes)

    def _send_get_receipts(self, block_hashes: Tuple[Hash32, ...]) -> None:
        cmd = GetReceipts(self.cmd_id_offset)
        header, body = cmd.encode(block_hashes)
        self.send(header, body)

    def send_receipts(self, receipts: List[List[Receipt]]) -> None:
        cmd = Receipts(self.cmd_id_offset)
        header, body = cmd.encode(receipts)
        self.send(header, body)

    #
    # Transactions
    #
    def send_transactions(self, transactions: List[BaseTransactionFields]) -> None:
        cmd = Transactions(self.cmd_id_offset)
        header, body = cmd.encode(transactions)
        self.send(header, body)
