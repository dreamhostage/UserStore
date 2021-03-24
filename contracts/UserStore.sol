pragma solidity 0.5.4;

//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.3.0/contracts/token/ERC721/ERC721.sol";
import "./ERC721/token/ERC721/ERC721.sol";

contract UserStore is ERC721 {
    
    uint256 ids = 0;
    
    struct keyInfo {
        uint256 id;
        string data;
        bool unique;
    }
    
    mapping(bytes32 => keyInfo) private keyData;
    
    function mintToken(string memory key, string memory data) public {
        require(keyData[keccak256(abi.encodePacked((key)))].unique != true);
        _mint(msg.sender, ids);
        keyData[keccak256(abi.encodePacked((key)))] = keyInfo(ids, data, true);
        ids++;
    }

    function getTokenData(string memory key) public view returns(string memory){
        return keyData[keccak256(abi.encodePacked((key)))].data;
    }
    
    function getTokenOwner(string memory key) public view returns(address){
        
        return ownerOf(keyData[keccak256(abi.encodePacked((key)))].id);
    }
    
    function transferToken(string memory key, address address_) public {
        
        require(msg.sender == ownerOf(keyData[keccak256(abi.encodePacked((key)))].id));
        transferFrom(msg.sender, address_, keyData[keccak256(abi.encodePacked((key)))].id);
    }
    
    function changeTokenData(string memory key, string memory data) public {
        
        require(msg.sender == ownerOf(keyData[keccak256(abi.encodePacked((key)))].id));
        keyData[keccak256(abi.encodePacked((key)))].data = data;
    }
}