#include <iostream>
#include <queue>
using namespace std;

// Define the structure for a binary tree node
struct Node {
    int data;
    Node* left;
    Node* right;
};

// Function to create a new binary tree node
Node* createNode(int data) {
    Node* newNode = new Node();
    if (!newNode) {
        cout << "Memory error\n";
        return NULL;
    }
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}

// Function to check if a binary tree is balanced
bool isTreeBalanced(Node* root) {
    if (root == NULL) {
        return true; // empty tree is balanced
    }

    queue<pair<Node*, int>> Q; // queue to store pairs of (node, depth)
    Q.push({root, 0});
    bool isBalanced = true;

    while (!Q.empty() && isBalanced) {
        Node* currentNode = Q.front().first;
        int currentDepth = Q.front().second;
        Q.pop();

        int leftDepth = 0;
        int rightDepth = 0;

        if (currentNode->left != NULL) {
            Q.push({currentNode->left, currentDepth + 1});
            leftDepth = getHeight(currentNode->left);
        }

        if (currentNode->right != NULL) {
            Q.push({currentNode->right, currentDepth + 1});
            rightDepth = getHeight(currentNode->right);
        }

        if (abs(leftDepth - rightDepth) > 1) {
            isBalanced = false;
        }
    }

    return isBalanced;
}

// Helper function to get the height of a tree
int getHeight(Node* root) {
    if (root == NULL) {
        return 0;
    }

    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);

    return max(leftHeight, rightHeight) + 1;
}

// Example usage:
int main() {
    Node* root = createNode(1);
    root->left = createNode(2);
    root->right = createNode(3);
    root->left->left = createNode(4);
    root->left->right = createNode(5);

    if (isTreeBalanced(root)) {
        cout << "The binary tree is balanced." << endl;
    } else {
        cout << "The binary tree is not balanced." << endl;
    }

    return 0;
}