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

bool isTreeBalanced(Node* root, int& height) {
    if (root == NULL) {
        height = 0;
        return true; // empty tree is balanced
    }

    int leftHeight = 0;
    int rightHeight = 0;

    if (!isTreeBalanced(root->left, leftHeight)) {
        return false;
    }

    if (!isTreeBalanced(root->right, rightHeight)) {
        return false;
    }

    height = max(leftHeight, rightHeight) + 1;

    if (abs(leftHeight - rightHeight) > 1) {
        return false;
    }

    return true;
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

    int height = 0;
    if (isTreeBalanced(root, height)) {
        cout << "The binary tree is balanced." << endl;
    } else {
        cout << "The binary tree is not balanced." << endl;
    }

    return 0;
}
