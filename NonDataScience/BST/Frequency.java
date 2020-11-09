import java.util.Comparator;
/**
 */
public class Frequency implements Comparator<Word> {
        @Override
        public int compare(Word w1, Word w2) {
               return -Integer.compare(w1.getFrequency(), w2.getFrequency());
        }
}
