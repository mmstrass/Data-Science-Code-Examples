import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.Scanner;
/**
 */
public class Index {
    public BST<Word> buildIndex(String fileName) {
            int lineNumber = 0;
            BST<Word> bst = new BST<Word>();
            Scanner scanner = null;
            if (fileName == null) {
                    return null;
            }
            if (fileName.length() == 0) {
                    return null;
            }
            try {
                    File file = new File(fileName);
                    scanner = new Scanner(file, "latin1");
                    while (scanner.hasNextLine()) {
                        lineNumber++;
                        String line = scanner.nextLine();
                        String[] wordsFromText = line.split("\\W");
                        for (String word : wordsFromText) {
                                if (checkString(word)) {
                                        Word w = new Word(word);
                                        if (bst.search(w) == null) {
                                                w.addToIndex(lineNumber);
                                                bst.insert(w);
                                        } else {
                                                Word tmp = bst.search(w);
                                                tmp.incrementFrequency();
                                                tmp.addToIndex(lineNumber);
                                        }
                            }
                    }
                }
            } catch (FileNotFoundException e) {
                System.err.println("Cannot find the file");
            } finally {
                if (scanner != null) {
                    scanner.close();
                }
            }
            return bst;
    }
    private boolean checkString(String text) {
            if (text.matches("^[a-zA-Z]+$")) {
                    return true;
            }
            if (text == " " || text == "") {
                    return false;
            }
            return false;
    }
    public BST<Word> buildIndex(String fileName, Comparator<Word> comparator) {
            int lineNumber = 0;
            BST<Word> bst = new BST<Word>(comparator);
            Scanner scanner = null;
            if (fileName == null) {
                    return null;
            }
            if (fileName.length() == 0) {
                    return null;
            }
            try {
                    File file = new File(fileName);
                    scanner = new Scanner(file, "latin1");
                    while (scanner.hasNextLine()) {
                        lineNumber++;
                        String line = scanner.nextLine();
                        String[] wordsFromText = line.split("\\W");
                        for (String word : wordsFromText) {
                                if (comparator.getClass().isInstance(new IgnoreCase())) {
                                        word = word.toLowerCase();
                                }
                                if (checkString(word)) {
                                        Word w = new Word(word);
                                        if (bst.search(w) == null) {
                                                w.addToIndex(lineNumber);
                                                bst.insert(w);
                                        } else {
                                                Word tmp = bst.search(w);
                                                tmp.incrementFrequency();
                                                tmp.addToIndex(lineNumber);
                                        }
                            }
                    }
                }
            } catch (FileNotFoundException e) {
                System.err.println("Cannot find the file");
            } finally {
                if (scanner != null) {
                    scanner.close();
                }
            }
            return bst;
    }

    public BST<Word> buildIndex(ArrayList<Word> list, Comparator<Word> comparator) {
            BST<Word> bst = new BST<Word>(comparator);
            if (list == null) {
                    return null;
            }
            if (list.size() == 0) {
                    return null;
            }
                        for (Word word : list) {
                                if (comparator.equals(new IgnoreCase())) {
                                        word.setWord(word.getWord().toLowerCase());
                                }
                                if (checkString(word.getWord())) {
                                        if (bst.search(word) == null) {
                                                bst.insert(word);
                                        }
                            }
                    }
            return bst;
    }
    public ArrayList<Word> sortByAlpha(BST<Word> tree) {
        /*
         * Even though there should be no ties with regard to words in BST,
         * in the spirit of using what you wrote,
         * use AlphaFreq comparator in this method.
         */
            ArrayList<Word> sorted = new ArrayList<Word>();
            Iterator<Word> iter = tree.iterator();
            while (iter.hasNext()) {
                    sorted.add(iter.next());
            }
            Collections.sort(sorted, new AlphaFreq());
            return sorted;
    }
    public ArrayList<Word> sortByFrequency(BST<Word> tree) {
            ArrayList<Word> sorted = new ArrayList<Word>();
            Iterator<Word> iter = tree.iterator();
            while (iter.hasNext()) {
                    sorted.add(iter.next());
            }
            Collections.sort(sorted, new Frequency());
            return sorted;
    }
    public ArrayList<Word> getHighestFrequency(BST<Word> tree) {
            ArrayList<Word> sorted = new ArrayList<Word>();
            Iterator<Word> iter = tree.iterator();
            while (iter.hasNext()) {
                    sorted.add(iter.next());
            }
            Collections.sort(sorted, new Frequency());
            int highestFreq = sorted.get(0).getFrequency();
            boolean end = false;
            int i = 0;
            while (!end && i < sorted.size()) {
                    if (sorted.get(i).getFrequency() != highestFreq) {
                            end = true;
                    } else {
                            i++;
                    }
            }
            ArrayList<Word> subSorted = new ArrayList<Word>(sorted.subList(0, i));
            return subSorted;
    }
}
