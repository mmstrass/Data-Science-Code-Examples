/**
 * 17-683 Data Structures for Application Programmers.
 * Homework Assignment 4: HashTable Implementation with linear probing
 *
 * Andrew ID: mstrasse
 * @author Molly Strasser
 */
public class MyHashTable implements MyHTInterface {

        /**
         * The DataItem array of the table.
         */
        // constructor for hashArray
        private DataItem[] hashArray;
        /*
         * global variable private int numOfColls global number of collisions to 0
         */
        private int numOfColls = 0; // this sets numOfColls
        /*
         * global variable private double size initialize global var for size to 0
         */
        private double size = 0; //sets size
        /*
         * global variable private double loadFactor initialize global var for size to 0.5
         */
        private double loadFactor = 0.5; //loadfactor for hash
        /*
         * global variable private static final DataItem DELETED initialize global final var for flag for deleted items
         */
        private static final DataItem DELETED = new DataItem("#DEL#"); //set the deleted flag
        /*
         * global variable private char [] alpha initialize array of letters
         */
        private char[] alpha = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}; //intialize arra to use
        /*
         * int N initialize global var for number for hashfunc
         */
        private static final int N = 27; //set factor to multiply by
        /*
         * constructor with no initial capacity
         */
        public MyHashTable() {
                hashArray = new DataItem[10];
        }
        /* constructor with initial capacity
         * @params: initialCap: initial capacity of the array
         */
        public MyHashTable(int initialCap) {
                if (initialCap <= 0) {
                        throw new RuntimeException();
                }
                hashArray = new DataItem[initialCap];
        }

        /**
         * Instead of using String's hashCode, you are to implement your own here.
         * You need to take the table length into your account in this method.
         *
         * In other words, you are to combine the following two steps into one step.
         * 1. converting Object into integer value
         * 2. compress into the table using modular hashing (division method)
         *
         * Helper method to hash a string for English lowercase alphabet and blank,
         * we have 27 total. But, you can assume that blank will not be added into
         * your table. Refer to the instructions for the definition of words.
         *
         * For example, "cats" : 3*27^3 + 1*27^2 + 20*27^1 + 19*27^0 = 60,337
         *
         * But, to make the hash process faster, Horner's method should be applied as follows;
         *
         * var4*n^4 + var3*n^3 + var2*n^2 + var1*n^1 + var0*n^0 can be rewritten as
         * (((var4*n + var3)*n + var2)*n + var1)*n + var0
         *
         * Note: You must use 27 for this homework.
         *
         * However, if you have time, I would encourage you to try with other
         * constant values than 27 and compare the results but it is not required.
         * @param input input string for which the hash value needs to be calculated
         * @return int hash value of the input string
         */
        private int hashFunc(String input) {
                int[] intRep = getIntRep(input); //get the integer representation of the string
                int hashVal = 0;  //set initial hashvalue to zero
                for (int i = 0; i < intRep.length; i++) { // iterate through the int array from the end to get the correct values for i
                        hashVal = hashVal * N + (Character.getNumericValue(input.charAt(i)) - 9); //intRep[i];
                        hashVal = (hashVal & 0x7FFFFFFF) % (hashArray.length); // need to use bitwise to get rid of negatives
                }
                return hashVal; //return this as the new index to initially try to store the value at
        }
        /*
         * @param String input input string for which the hash value needs to be calculated
         * @return int[] representation of the string
         */
        private int[] getIntRep(String input) {
                int[] intRep = new int[input.length()]; //create a new integer array of length of the string
                char[] tmp = input.toCharArray(); //convert string to char array to iterate through
                for (int i = 0; i < tmp.length; i++) {
                        for (int a = 0; a < alpha.length; a++) {
                                if (alpha[a] == tmp[i]) { //find the index where that value is kept
                                        intRep[i] = a + 1; //increment by 1 to get the correct repres
                                }
                        }
                }
                return intRep; //return the int array representing the string
        }

        /**
         * doubles array length and rehash items whenever the load factor is reached.
         * Note: do not include the number of deleted spaces to check the load factor.
         * Remember that deleted spaces are available for insertion.
         */
        private void rehash() {
                int newSize = hashArray.length * 2; // double the array length
                //while the new size isn't a prime value, increment size and recompute
                while (!isPrime(newSize)) {
                        newSize = newSize + 1;
                }
                DataItem[] newArray = new DataItem[newSize]; //create a new array with the prime length
                DataItem[] temp = tempClone(); // create a new array that will temporarily store the hashArray values
                hashArray = newArray; // set the hashArray to the bigger array now its values have been copied to temp
                for (int i = 0; i < temp.length; i++) { //iterate through the temp array containing the values of the old hashArray
                        DataItem val = temp[i]; // create di to store the value in temp
                        int index = hashValue(val.value); // compute hash of the value to find the new index to start with
                        if (hashArray[index] != null) {
                                numOfColls++; // found an empty index. Add the value here
                        }
                        while (hashArray[index] != null) { // if the array at the index is not empty
                                //increment index, we do not need to check for duplicate values because they should not exist in temp
                                index = index + 1;
                                if (index > hashArray.length - 1) { // if index is greater than the length-1 we are at the end of the array
                                        index = index % hashArray.length; // set index to its value mod the length to wrap around
                                }
                        }
                        hashArray[index] = val; // found an empty index. Add the value here
                }
                System.out.println("Rehashing " + (int) (size) + " items. The new size is " + hashArray.length);
        }
        /*
         * @param p new size of the array
         * @return boolean false if not a prime true if a prime
         */
        private boolean isPrime(int p) {
                if (p % 2 == 0) {
                        return false;
                }
                for (int i = p / 2; i > 2; i--) {
                        if (p % i == 0) {
                                return false;
                        }
                }
                return true;
        }

        /*
         * clone the current hashArray so that when we rehash the
         * array we are calculating the correct new indexes for the DataItems
         * @param none
         * @return DataItem array of the hasharray
         */
        private DataItem[]  tempClone() {
                DataItem[] temp = new DataItem[(int) size]; //create new array of length of the number of items in the current hash array
                int s = 0; // set a variable so we can iterate through temp as we add new values in to the array
                for (int i = 0; i < hashArray.length; i++) { // iterate through hashArray to find where we have DataItems stored
                        // if the hashArray at this index is NOT null and it is NOT a deleted flag
                        if (hashArray[i] != null && hashArray[i] != DELETED) {
                                DataItem t = hashArray[i]; //set temporary dataitem equal to the di stored at this index
                                temp[s] = t; // set temp array equal to the dataitem stored at index i in hashArray
                                s++; //increment s so that we store the next hashArray item found at the next index in temp
                        }
                }
                return temp; //return array
        }
        @Override
        public void insert(String value) {
                if (value == null || value == "#DEL#") {
                        return;
                }
                value = value.trim();
                if (!checkString(value)) { //check to make sure string meets reqs
                        return; //if not return
                }
                value = value.toLowerCase();
                double load = size / hashArray.length; // compute the load factor of the array
                // if the load factor is greater than the set load factor rehash the array
                if (load > loadFactor) {
                        numOfColls = 0;
                        rehash();
                }
                int index = hashValue(value); // find the starting index for the new value
                if (hashArray[index] == null || hashArray[index] == DELETED) {
                        hashArray[index] = new DataItem(value); // we have an open index add the new element here
                        size++; // increment the variable for size
                        return;
                }
                while (hashArray[index] != null && hashArray[index] != DELETED) {
                                if (hashArray[index].value.equals(value)) { // if the value in the DataItem is equal to the value we are adding
                                        hashArray[index].frequency += 1; //update the frequency
                                        return;
                                }
                                index = index + 1;
                                if (index > hashArray.length - 1) { // if we have reached the end of the array
                                        index = index % hashArray.length; // wrap around
                                }
                        }
                hashArray[index] = new DataItem(value); // we have an open index add the new element here
                numOfColls += 1;
                size++; // increment the variable for size
        }

        /**checks to make sure the input string is only alpha characters.
         * @param text String to check
         * @return True if only alpha char, false otherwise
         */
        private boolean checkString(String text) {
                text = text.toLowerCase();
                if (text.matches("^[a-zA-Z]+$")) {
                        return true;
                }
                return false;
        }

        @Override
        public int size() {
                return (int) size;
        }

        @Override
        public void display() {
                for (int i = 0; i < hashArray.length; i++) { //iterate through the array
                        if (hashArray[i] != null && hashArray[i] != DELETED) { //if it is not null then print out the DataItem
                                System.out.print("[" + hashArray[i].value + ", " + hashArray[i].frequency + "] ");
                        } else if (hashArray[i] == DELETED) {
                                System.out.print(hashArray[i].value);
                        } else { // if it is null print out asterix
                                System.out.print(" ** ");
                        }
                }
                System.out.println("");
        }

        @Override
        public boolean contains(String key) {
                if (key == null || !checkString(key)) {
                        return false;
                }
                if (key == "#DEL#") {
                        return false;
                }
                int index = hashValue(key); // find the index that this value would have initially been tried to be stored at
                //if this index isn't null (does not include deleted bc a value could have been deleted after the key was added)
                if (hashArray[index] == null) {
                        return false;
                }
                int tmp = 0;
                while (hashArray[index] != null && tmp < hashArray.length) {
                        if (hashArray[index].value.equals(key)) { // check to see if the value equals the key
                                return true;
                        }
                        // continue down the array
                        index = index + 1; // increment the index to check
                        tmp = tmp + 1;
                        if (index > hashArray.length - 1) { // wrap around
                                index = index % hashArray.length;
                        }
                }
                return false; // it is not in the array
        }

        @Override
        public int numOfCollisions() {
                return numOfColls;
        }

        @Override
        public int hashValue(String value) {
                if (value == null) {
                        throw new RuntimeException();
                }
                return hashFunc(value);
        }

        @Override
        public int showFrequency(String key) {
                if (key == null || !checkString(key)) {
                        return 0;
                }
                int index = hashValue(key); // find the initial index that we would try to store key
                int counter = 0;
                while (hashArray[index] != null && counter < hashArray.length) { // while there is a value in the array
                        //check to see if the value at that index is equal to the key
                        if (hashArray[index].value.equals(key)) {
                                return hashArray[index].frequency; // return the frequency count for the value
                        }
                        index = index + 1; // else continue down the array
                        counter++;
                        // if we reach the end of the array without hitting a null value wrap around to the front
                        if (index > hashArray.length - 1) {
                                index = index % hashArray.length;
                        }
                }
                return 0; //value does not exist in the array
        }

        @Override
        public String remove(String key) {
                if (key == null || !checkString(key) || size == 0) {
                        return null;
                }
                int index = hashValue(key); // find the initial index to start at
                int counter = 0;
                if (hashArray[index] == null) {
                        return null;
                }
                while (counter < hashArray.length && hashArray[index] != null) {
                                if (hashArray[index].value.equals(key)) { // if the value is being stored at this index
                                        hashArray[index] = DELETED; // set the array at this index to the deleted flag
                                        size--;
                                        return key; // return the key value
                                }
                                index = index++;
                                if (index > hashArray.length - 1) {
                                        index = index % hashArray.length; // wrap around to the front
                                }
                                counter = counter + 1; // increment index to continue down the array until we hit a null value
                        }
                return null; //hit a null value and found nothing to remove
        }
        /**
         * private static data item nested class.
         */
        private static class DataItem {
                /**
                 * String value.
                 */
                private String value;
                /**
                 * String value's frequency.
                 */
                private int frequency;

                DataItem() {
                        value = null;
                        frequency = -1;
                }

                DataItem(String v, int f) {
                        value = v;
                        frequency = f;
                }

                DataItem(String v) {
                        value = v;
                        frequency = 1;
                }
        }
}
