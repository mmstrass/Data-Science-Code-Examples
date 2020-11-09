import java.util.Comparator;
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Stack;
/**
 * Building Index using BST
 * @param <T> object type
 */
public class BST<T extends Comparable<T>> implements Iterable<T>, BSTInterface<T> {
        /**
         * Node<T> to use as the root of the BST.
         */
    private Node<T> root;
    /**
     * comparator to be used.
     */
    private Comparator<T> comparator;
    public BST() {
        this(null);
    }
    public BST(Comparator<T> comp) {
        comparator = comp;
        root = null;
    }
    public Comparator<T> comparator() {
        return comparator;
    }
    public T getRoot() {
        if (root == null) {
                return null;
        }
        return root.data;
    }
    public int getHeight() {
            if (root == null) {
                    return 0;
            }
        return getHeightHelper(root);
    }
    private int getHeightHelper(Node<T> curr) {
            if (curr == null) {
                    return -1;
            }
            int lHeight = getHeightHelper(curr.left);
            int rHeight = getHeightHelper(curr.right);
            if (lHeight > rHeight) {
                    return 1 + lHeight;
            } else {
                    return 1 + rHeight;
            }
    }
    public int getNumberOfNodes() {
        return getNumberHelper(root);
    }
    private int getNumberHelper(Node<T> curr) {
           if (curr == null) {
                   return 0;
           }
           int lLeaves = getNumberHelper(curr.left);
           int rLeaves = getNumberHelper(curr.right);
           return 1 + lLeaves + rLeaves;
    }
    @Override
    public T search(T toSearch) {
        return searchHelper(root, toSearch);
    }
    private T searchHelper(Node<T> curr, T toSearch) {
            if (curr == null) {
                    return null;
            } else if (compare(curr.data, toSearch) != 0) {
                    if (compare(curr.data, toSearch) < 0) {
                            return searchHelper(curr.right, toSearch);
                    } else {
                            return searchHelper(curr.left, toSearch);
                    }
            }
            return (T) curr.data;
    }
    private int compare(T item1, T item2) {
            if (comparator == null) {
                    return item1.compareTo(item2);
            } else {
                    return comparator.compare(item1, item2);
            }
    }
    @Override
    public void insert(T toInsert) {
        if (root == null) {
                root = new Node<T>(toInsert);
                return;
        }
        insertHelper(toInsert, root);
    }
    private void insertHelper(T toInsert, Node<T> curr) {
            if (compare(curr.data, toInsert) == 0) {
                    return;
            }
            if (compare(curr.data, toInsert) < 0) {
                    if (curr.right == null) {
                            curr.right = new Node<T>(toInsert);
                            return;
                    }
                    insertHelper(toInsert, curr.right);
            } else {
                    if (curr.left == null) {
                            curr.left = new Node<T>(toInsert);
                            return;
                    }
                    insertHelper(toInsert, curr.left);
            }
    }
    @Override
    public Iterator<T> iterator() {
            return new BSTIterator();
    }
    private class BSTIterator implements Iterator<T> {
            /**
             * stack data object to hold objects from bst.
             */
            private Stack<Node<T>> stack;
            /**
             * nextNode node of object type T.
             */
            private Node<T> nextNode;
            BSTIterator() {
                    nextNode = root;
                    stack = new Stack<Node<T>>();
                    while (nextNode != null) {
                        stack.push(nextNode);
                        nextNode = nextNode.left;
                }
            }
            @Override
            public boolean hasNext() {
                    return !stack.isEmpty();
            }
            @Override
            public T next() {
                    if (!hasNext()) {
                            throw new NoSuchElementException();
                    }
                   Node<T> n = stack.pop();
                   T val = n.data;
                   if (n.right != null) {
                           n = n.right;
                           while (n != null) {
                                   stack.push(n);
                                   n = n.left;
                           }
                   }
                  return val;
            }
    }
    private static class Node<T> {
        /**
         * data object type T.
         */
        private T data;
        /**
         * left node of object type T hold left leaf.
         */
        private Node<T> left;
        /**
         * right node of object type T hold right leaf.
         */
        private Node<T> right;

        Node(T d) {
            this(d, null, null);
        }

        Node(T d, Node<T> l, Node<T> r) {
            data = d;
            left = l;
            right = r;
        }
    }

}
