/**
 * Listen to when network is updated in the network editor
 */
document.addEventListener('updateNodeList', (nodeList) => this.updateNodeList(nodeList?.detail));

function updateNodeList(nodeList) {
  var nodeListContainer = $("#node-list-container");

  // make sure that the node list is an iterable array
  if (!nodeList || !Array.isArray(nodeList) || !nodeList.length) {
    return;
  }

  nodeList.forEach(node => {
    // add node to list
    var nodeListItem = document.createElement("div");
    nodeListItem.id = node?.uuid;
    nodeListItem.innerHTML = node?.name;

    nodeListContainer.append(nodeListItem);
  });
}