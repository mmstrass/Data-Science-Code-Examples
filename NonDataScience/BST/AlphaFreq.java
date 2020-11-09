import java.util.Comparator;
/**
 */
public class AlphaFreq implements Comparator<Word> {
        @Override
        public int compare(Word w1, Word w2) {
                int resultIC = w1.getWord().compareTo(w2.getWord());
                if (resultIC == 0) {
                        return Integer.compare(w1.getFrequency(), w2.getFrequency());
                }
                return resultIC;
        }
}
