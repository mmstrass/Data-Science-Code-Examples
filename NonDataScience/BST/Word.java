import java.util.HashSet;
import java.util.Set;
/**
 */
public class Word implements Comparable<Word> {
        /**
         * word string global.
         */
        private String word;
        /**
         * index Set<Integer> to hold line numbers.
         */
        private Set<Integer> index;
        /**
         * frequency int to keep track of number of times word occurs.
         */
        private int frequency;
        /**
         * constructor for Word object.
         * @param w word to add
         */
        public Word(String w) {
                frequency = 1;
                index = new HashSet<Integer>();
                word = w;
        }
        /**
         * Adds new line number to Index set.
         * @param idx integer of line number word occurs at
         */
        public void addToIndex(Integer idx) {
                index.add(idx);
        }
        /**
         * @return Index set.
         */
        public Set<Integer> getIndex() {
                return this.index;
        }
        /**
         * Allows word to be set for Word object.
         * @param w string word to be added.
         */
        public void setWord(String w) {
                word = w;
        }
        /**
         * @return word.
         */
        public String getWord() {
                return word;
        }
        /**
         * Set frequency for a word.
         * @param freq int to be added.
         */
        public void setFrequency(int freq) {
                frequency = freq;
        }
        /**
         * @return frequency.
         */
        public int getFrequency() {
                return frequency;
        }
        /**
         * Increments frequency by one.
         */
        public void incrementFrequency() {
                frequency++;
        }
        /**
         * Compares two words.
         * @params: Word w object to be compared with
         */
        @Override
        public int compareTo(Word w) {
                return word.compareTo(w.getWord());
        }
        /**
         * Returns Word object as a string.
         */
        @Override
        public String toString() {
                return word + " " + frequency + " " + index;
        }
}

