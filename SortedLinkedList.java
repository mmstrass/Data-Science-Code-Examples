import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * 
 * @author Molly Strasser
 */

public class SortedLinkedList implements MyListInterface {
        /**
         * constant for head of the linkedlist.
         */
        private Node<String> head;
        /**
         * no-arg constructor that instantiate linkedlist.
         */
        public SortedLinkedList() {
            head = null;
        }
        /**Constructor with string array.
         * @param str string array with values for linkedlist
         */
        public SortedLinkedList(String[] str) {
                if (str == null) {
                        head = null;
                        return;
                        } else {
                                helperSortedLinkedList(str, 0);
                        }
        }
        private void helperSortedLinkedList(String[] str, int i) {
                if (i < str.length) {
                        add(str[i]);
                        i += 1;
                        helperSortedLinkedList(str, i);
                }
                return;
        }
        @Override
        public void add(String value) {
                if (value == null) {
                        return;
                        }
                add(value, null, head);
                return;
        }
       //helper method for add
       private void add(String value, Node<String> prev, Node<String> next) {
            if (head == null) {
                    head = new Node<String>(value, null);
                    return;
                    }
            if (next.data.compareToIgnoreCase(value) == 0) {
                    return;
                    }
            if (next.data.compareToIgnoreCase(value) > 0) {
                    Node<String> n = new Node<String>(value, next);
                    if (prev != null) {
                            prev.next = n;
                            }
                    if (prev == null) {
                            head = n;
                            }
                    return;
                    }
            if (next.next == null) {
                    Node<String> n = new Node<String>(value, null);
                    next.next = n;
                    return;
                    }
            if (next.data.compareTo(value) < 0) {
                    add(value, next, next.next);
                    }
            return;
       }
        @Override
        public int size() {
               Node<String> n = head;
               int count = 0;
               return size(head, count);
        }
        private int size(Node<String> n, int count) {
                if (n == null) {
                        return count;
                        } else if (head.next == null) {
                        return 1;
                        } else {
                        count++;
                        return size(n.next, count);
                        }
        }

        @Override
        public void display() {
                display(head);
        }
        private void display(Node<String> curr) {
                if (head == null) {
                        return;
                        } else if (curr.data.equalsIgnoreCase(head.data) && curr.next == null) {
                        System.out.println("[" + head.data + "]");
                        return;
                        } else if (curr.data.equalsIgnoreCase(head.data)) {
                       System.out.print("[" + head.data + ", ");
                       display(curr.next);
                       } else if (curr.next == null) {
                       System.out.print(curr.data + "]\n");
                       return;
                       } else {
                       System.out.print(curr.data + ", ");
                       display(curr.next);
                       }
        }
        @Override
        public boolean contains(String key) {
                return contains(key, head);
        }
        private boolean contains(String key, Node<String> curr) {
                if (curr.data.equalsIgnoreCase(key)) {
                        return true;
                        }
                if (curr.next == null) {
                        return false;
                } else {
                        return contains(key, curr.next);
                        }
        }
        @Override
        public boolean isEmpty() {
                if (head == null) {
                        return true;
                        }
                return false;
        }
        @Override
        public String removeFirst() {
                if (head == null) {
                        return null;
                        }
                String data = head.data;
                if (head.next != null) {
                        head = head.next;
                } else {
                        head = null;
                        }
                return data;
        }
        @Override
        public String removeAt(int index) {
                if (index >= size() || index < 0) {
                        throw new RuntimeException();
                        } else {
                        return removeAt(index, 0, null, head);
                        }
        }
        private String removeAt(int index, int count, Node<String> prev, Node<String> curr) {
                if (index == 0) { // if we are removing the first entry in the list
                        if (curr != null) {
                                head = curr.next; // set the head to the new head
                                return curr.data;
                                }
                        return null;
                        }
                if (curr.next == null) { // if we are at the end of the list
                        prev.next = null;
                        return curr.data; // return the data from the removed node
                        } else if (curr.next != null) { // if we have not reached the end of the list
                        if (index == count) { // if we have found the index we want
                            prev.next = curr.next; // set the previous node to point at the next node
                            return curr.data;
                    } else {
                            count += 1;
                            return removeAt(index, count, curr, curr.next); //recurse
                            }
                        }
                return null;
        }
        /**
         * Inner (non-static) class for Iterator implementation.
         */
        private class LinkedListIterator implements Iterator<String> {
            /**
             * Reference to nextNode to access.
             */
            private Node<String> nextNode;

            /**
             * No-arg constructor that starts the iteration from the head.
             */
            LinkedListIterator() {
                // access to the head instance variable of the Outer class
                nextNode = head;
            }

            /**
             * Checks whether there is next element or not.
             *
             * @return true if there is next element or false if not
             */
            @Override
            public boolean hasNext() {
                return nextNode != null;
            }

            /**
             * Returns next element in the sequence and moves forward.
             *
             * @return next element (data)
             * @throws throws NoSuchElementException if there is no element.
             */
            @Override
            public String next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                String result = nextNode.data;
                nextNode = nextNode.next;
                return result;
            }
        }
        /**
         * Static nested class for Node.
         *
         * @param <AnyType> Generic type of item
         */
        private static class Node<AnyType> {
            /**
             * data of a node (item).
             */
            private AnyType data;
            /**
             * Reference to next node.
             */
            private Node<AnyType> next;

            /**
             * Construct a new node with data and next node reference.
             *
             * @param newData data of the node (item)
             * @param newNext reference to next node
             */
            Node(AnyType newData, Node<AnyType> newNext) {
                data = newData;
                next = newNext;
            }
        }
}



