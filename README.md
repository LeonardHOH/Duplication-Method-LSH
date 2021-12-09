# Duplication-Method-LSH
Duplication Method using LSH and Jaccard Similarity
What is it about?
Due to the growing number of Web shops, aggregating product data is becoming more important. To automatically aggregate data from Web shops, it is necessary to use duplicate detection. In order to finds these pairs, Locality Sensitive Hashing (LSH) and min-hashing have been used in the code. The data set consists of 1624 products (TV's) from four different Web shops. The binary vectors are created by using only modelwords with a numerical part and a qualitative part. Furthermore, the brands of the products (if any) are included and the data has been cleaned. At last, the candidate pairs are approached as a classification problem with the use of Jaccard Similarity. T
How is the Code Structured?
In the first sections the data is loaded. 
The sections afterwards the data is cleaned. 
Then the model words form the product attribute values and the titles are combined together
Afterwards, model words are created from wich binary vectors are made which consitis out of zeros and ones.
Then these are min-hashed into a signature matrix with dimensions the number of permutations versus the number of products
Then LSH has been used, where bucket numbers are created by "summing" the rows of a certain band. This has been done for mulitple number of bands.
Accordlingy, the Jaccard Similirity between the candidate pairs is calculated for a certain threshold. 
Then the false negatives, false positives, true positives and true negatives are determined to calculate recall and precision. 
When these are calculated, the F-1 measure will be calculated and the F-1 measure and recall and precision will be plotted against the fraction for LSH and the complete method. 
I have programmed this with Sweder Steensma. 
