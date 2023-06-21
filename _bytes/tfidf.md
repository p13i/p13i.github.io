---
layout: post
title: "TFiDF"
date: 2017-08-24
description: "Term Frequency - Inverse Document Frequency"
image: https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/remembrance-agent/blob/master/src/main/java/io/p13i/ra/utils/TFIDFCalculator.java
---

```java
/**
 * Computes TFiDF
 *
 * @author Mohamed Guendouz
 * @author Pramod Kotipalli (@p13i)
 */
public class TFIDFCalculator {
    /**
     * @param doc  list of strings
     * @param term String represents a term
     * @return term frequency of term in document
     */
    public static double tf(AbstractDocument doc, String term) {
        int result = 0;
        List<String> wordVector = doc.getWordVector();
        for (String word : wordVector) {
            if (term.equalsIgnoreCase(word))
                result++;
        }
        return result / (double) wordVector.size();
    }

    /**
     * @param docs list of list of strings represents the dataset
     * @param term String represents a term
     * @return the inverse term frequency of term in documents
     */
    private static double idf(Iterable<AbstractDocument> docs, String term) {
        int n = 0;
        int N = 0;
        for (AbstractDocument doc : docs) {
            List<String> wordVector = doc.getWordVector();
            for (String word : wordVector) {
                if (term.equalsIgnoreCase(word)) {
                    n++;
                    break;
                }
            }
            N++;
        }
        return Math.log((double) N / (double) n);
    }

    /**
     * Computes the TFiDF of a query for a given document
     *
     * @param queryTerm term
     * @param document  a text document
     * @param documents all documents
     * @return the TF-IDF of term
     */
    public static double tfIdf(String queryTerm, AbstractDocument document, Iterable<AbstractDocument> documents) {
        return tf(document, queryTerm) * idf(documents, queryTerm);
    }
}
```
