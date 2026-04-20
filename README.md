# Data Structures: Assignment 1 - Sorting Algorithm Comparison

## Student Names
- Omer Pimontel
- Ori Gurwicz

## Selected Algorithms
1. Bubble Sort
2. Merge Sort
3. Quick Sort

![sorting_table](Sorting_table.png)

## Experiment Results

### Result 1: Random Arrays

![result1](result1.png)

![result1_table](result1_table.png)

This experiment compares the three sorting algorithms on randomly shuffled arrays of increasing size.

**Observations:**
- **Bubble Sort** - shows a clear O(n²) growth pattern, with exponential increase in runtime as array size increases.
- **Merge Sort** - maintains a consistent O(n log n) behavior, showing much slower growth.
- **Quick Sort** - also demonstrates O(n log n), similar to Merge Sort.

Bubble sort quickly detaches from the algorithms that are better suited for this case and the gap only widens as arrays get bigger, 
showing exactly why Bubble sort (and other O(n²) algo's) are inferior to divide and conquer algorithms when using large datasets.

All algorithms clearly exhibit the average runtime complexity we expect them to!

### Result 2: Nearly-Sorted Arrays with 5% / 20% Noise

### 5% :


![result2](result2.png)

![result2_table](result2_table.png)

### 20% :

![result2](result3.png)

![result2_table](result3_table.png)


This experiment tests the same algorithms on nearly sorted arrays where 5% / 20% of the elements are randomly shuffled.

**Observations:**
- **Bubble Sort** maintains a general O(n²) behavior but displays improvement as a larger portions of the array are sorted.
- **Merge Sort** remains unchanged, as it always divides and merges regardless of input order. Its time complexity is strictly O(nlogn) in all cases.
- **Quick Sort** performs only slightly better to the random case. Standard Quick Sort can degrade to O(n²) on already sorted arrays depending on pivot selection but choosing the middle element as the pivot (as implemented here)
prevents this degradation on nearly sorted data, maintaining its efficient O(nlogn) average-case performance.

The presence of partial order (5% noise) helps Bubble Sort but doesn't fundamentally change the ranking.

The data confirms that even with partially sorted input, the algorithmic complexity dominates performance.

## Conclusion

This assignment demonstrates that algorithmic complexity is far more important than implementation details when dealing with large datasets. The O(n log n) algorithms significantly outperform O(n²) algorithms, with the performance gap increasing dramatically with array size. Even though Bubble Sort is simpler to implement, the practical advantages of using divide and conquer algorithms like Merge Sort or Quick Sort are undeniable.

// The added tables include numerical data that aided us in perceiving the runtime comparisons between algorithms since the O(nlogn) have a barely
noticeable difference (if any).

