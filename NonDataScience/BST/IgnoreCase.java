import java.util.Comparator;
/**
 */
public class IgnoreCase implements Comparator<Word> {
        @Override
        public int compare(Word w1, Word w2) {
                return w1.getWord().toLowerCase().compareTo(w2.getWord().toLowerCase());
        }
}
