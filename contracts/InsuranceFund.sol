// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.10;

import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/access/Ownable.sol";
import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC20/utils/SafeERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC721/IERC721.sol";
import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/token/ERC1155/IERC1155.sol";

/// @title Lido Insurance Fund
/// @author mymphe
/// @notice serves as a vault for Lido insurance funds; `owner` has full access
contract InsuranceFund is Ownable {
    using SafeERC20 for IERC20;

    event EtherTransferred(address indexed _recipient, uint256 _amount);
    event ERC20Transferred(
        address indexed _token,
        address indexed _recipient,
        uint256 _amount
    );
    event ERC721Transferred(
        address indexed _token,
        address indexed _recipient,
        uint256 _tokenId,
        bytes _data
    );
    event ERC1155Transferred(
        address indexed _token,
        address indexed _recipient,
        uint256 _tokenId,
        uint256 _amount
    );

    constructor(address _owner) {
        transferOwnership(_owner);
    }

    /// @notice prevents burn for recovery functions
    /// @dev checks for zero address and reverts if true
    /// @param _recipient address of the recovery recipient
    modifier burnDisallowed(address _recipient) {
        require(_recipient != address(0), "NO BURN");
        _;
    }

    /// @notice prevents `owner` from renouncing ownership and potentially locking assets forever
    /// @dev overrides Ownable's `renounceOwnership` to always revert
    function renounceOwnership() public pure override {
        revert("DISABLED");
    }

    /// @notice transfers ether from this contract
    /// @dev using the safer `call` instead of `transfer`
    /// @param _recipient address to transfer ether to
    /// @param _amount amount of ether to transfer
    function transferEther(address _recipient, uint256 _amount)
        external
        onlyOwner
        burnDisallowed(_recipient)
    {
        (bool success, ) = _recipient.call{value: _amount}("");
        require(success, "TRANSFER FAILED");
        emit EtherTransferred(_recipient, _amount);
    }

    /// @notice transfer an ERC20 token from this contract
    /// @dev SafeERC20.safeTransfer doesn't return a bool as it performs an internal `require` check
    /// @param _token address of the ERC20 token
    /// @param _recipient address to transfer the tokens to
    /// @param _amount amount of tokens to transfer
    function transferERC20(
        address _token,
        address _recipient,
        uint256 _amount
    ) external onlyOwner burnDisallowed(_recipient) {
        IERC20(_token).safeTransfer(_recipient, _amount);
        emit ERC20Transferred(_token, _recipient, _amount);
    }

    /// @notice transfer an ERC721 token from this contract
    /// @dev IERC721.safeTransferFrom doesn't return a bool as it performs an internal `require` check
    /// @param _token address of the ERC721 token
    /// @param _tokenId id of the individual token
    /// @param _recipient address to transfer the token to
    function transferERC721(
        address _token,
        address _recipient,
        uint256 _tokenId,
        bytes memory _data
    ) external onlyOwner burnDisallowed(_recipient) {
        IERC721(_token).safeTransferFrom(
            address(this),
            _recipient,
            _tokenId,
            _data
        );
        emit ERC721Transferred(_token, _recipient, _tokenId, _data);
    }

    /// @notice recover an ERC1155 token on this contract's balance as the owner
    /// @dev IERC1155.safeTransferFrom doesn't return a bool as it performs an internal `require` check
    /// @param _token address of the ERC1155 token that is being recovered
    /// @param _tokenId id of the individual token to transfer
    /// @param _recipient address to transfer the token to
    function transferERC1155(
        address _token,
        address _recipient,
        uint256 _tokenId
    ) external onlyOwner burnDisallowed(_recipient) {
        uint256 amount = IERC1155(_token).balanceOf(address(this), _tokenId);
        IERC1155(_token).safeTransferFrom(
            address(this),
            _recipient,
            _tokenId,
            amount,
            ""
        );
        emit ERC1155Transferred(_token, _recipient, _tokenId, amount);
    }
}
