#include <stdlib.h>
#include "checker.h"

#define COMPLEXITY 10
#define EXPECTED_CHECKSUM 457981248

struct tree_node {
    struct tree_node *left;
    struct tree_node *right;
    int leaf_id;
};

static struct tree_node *root = 0;

struct tree_node *get_root() {
    return root;
}

static unsigned int rnd_state = 0;

unsigned int rnd() {
    rnd_state = 134775813 * rnd_state + 1;
    return rnd_state;
}

void reset_rnd() {
    rnd_state = 0;
}

unsigned int get_leaf_id(struct tree_node *node, int code) {
    if (code < 1) return 0;
    struct tree_node *current_node = node;
    while (current_node->left != 0 && current_node->right != 0) {
        if ((code & 1) == 0) {
            current_node = current_node->left;
        } else {
            current_node = current_node->right;
        }
        code >>= 1;
    }
    return current_node->leaf_id;
}

//
// depth = 0 -> leaf (num of levels = 1)
// depth = 1 -> node with 2 leafs (num of levels = 2)
//
struct tree_node *alloc_tree(int depth) {
    struct tree_node *node = (struct tree_node *) malloc(sizeof(struct tree_node));
    node->leaf_id = 0;
    node->left = 0;
    node->right = 0;
    if (depth != 0) {
        node->left = alloc_tree(depth - 1);
        node->right = alloc_tree(depth - 1);
    } else {
        node->leaf_id = rnd();
    }
    return node;
}

void destroy_tree(struct tree_node *treeNode) {
    if (treeNode->left != 0) {
        destroy_tree(treeNode->left);
    }
    if (treeNode->right != 0) {
        destroy_tree(treeNode->right);
    }
    free(treeNode);
}

void rebuild_root() {
    if (root != 0) {
        destroy_tree(root);
    }
    root = alloc_tree(COMPLEXITY);
}

static unsigned int checksum = 0;

void add_code(int code) {
    rebuild_root();
    checksum ^= get_leaf_id(root, code);
}

#ifdef DEBUG
unsigned int debug_get_checksum() {
    return checksum;
}
#endif

bool check_code() {
    bool result = checksum == EXPECTED_CHECKSUM;
    checksum = 0;
    reset_rnd();
    return result;
}