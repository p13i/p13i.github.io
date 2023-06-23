---
layout: post
title: "LRU cache"
programming_language: "csharp"
date: 2020-02-13
description: "For interview prep, why else?"
image: https://user-images.githubusercontent.com/13140065/169116098-56d65621-69f3-4507-82e4-aaefe55986c9.png
downloads:
  - name: "💻 GitHub source"
    url: https://github.com/p13i/CSP/blob/master/Source/CSP/Solvers.cs#L39-L71
---

```csharp
public class LRUCache<K, V> : ILRUCache<K, V>
{
    public int Capacity { get; private set; }

    private readonly IDictionary<K, Node<K, V>> Cache = new Dictionary<K, Node<K, V>>();
    private Node<K, V> LeastRecentlyUsed;
    private Node<K, V> MostRecentlyUsed;

    public LRUCache(int capacity)
    {
        if (capacity <= 0)
        {
            throw new ArgumentOutOfRangeException($"{nameof(capacity)} must be positive");
        }

        Capacity = capacity;
    }

    public V Get(K key)
    {
        if (key == null)
        {
            throw new ArgumentNullException($"{nameof(key)} must not be null");
        }

        if (this.Cache.Count == 0)
        {
            throw new InvalidOperationException("cache is empty");
        }

        if (!this.Cache.ContainsKey(key))
        {
            throw new KeyNotFoundException($"{nameof(key)} of value {key.ToString()} not found in cache");
        }

        Node<K, V> node = this.Cache[key];

        // Shortcut if the node is the MRU. No adjustments needed
        if (key.Equals(this.MostRecentlyUsed.Key))
        {
            return node.Value;
        }

        // Special case for the LRU
        if (key.Equals(this.LeastRecentlyUsed.Key))
        {
            // Set the new LRU
            Node<K, V> nextLRU = node.Next;
            nextLRU.Previous = null;
            this.LeastRecentlyUsed = nextLRU;
        }
        else // the node is in the middle, not the MRU or LRU
        {
            // Remove the node from the list by connecting the next and previous nodes to each other
            Node<K, V> nextNode = node.Next;
            Node<K, V> previousNode = node.Previous;
            nextNode.Previous = previousNode;
            previousNode.Next = nextNode;
        }

        // Set the new MRU
        this.MostRecentlyUsed.Next = node;
        node.Previous = this.MostRecentlyUsed;
        this.MostRecentlyUsed = node;

        return node.Value;
    }

    public void Put(K key, V value)
    {
        if (key == null)
        {
            throw new ArgumentNullException($"{nameof(key)} must not be null");
        }

        // Remove the existing entry if it exists
        if (this.Cache.ContainsKey(key))
        {
            this.Delete(key);
        }

        // If the cache is at capacity, remove the LRU
        if (this.Cache.Count == this.Capacity)
        {
            this.Delete(this.LeastRecentlyUsed.Key);
        }

        Node<K, V> newNode = new Node<K, V>(key, value);

        // Special case for an empty cache
        if (this.Cache.Count == 0)
        {
            // Set this node to be the LRU and MRU
            this.LeastRecentlyUsed = newNode;
            this.MostRecentlyUsed = newNode;
        }
        else
        {
            // Move this to be the new MRU and adjust the old MRU
            this.MostRecentlyUsed.Next = newNode;
            newNode.Previous = this.MostRecentlyUsed;
            this.MostRecentlyUsed = newNode;
        }

        this.Cache[key] = newNode;
    }

    public void Delete(K key)
    {
        if (key == null)
        {
            throw new ArgumentNullException($"{nameof(key)} must not be null");
        }

        // Also covers the case that the cache is empty
        if (!this.Cache.ContainsKey(key))
        {
            throw new KeyNotFoundException($"{nameof(key)} of value {key.ToString()} not found in cache");
        }

        // Special case for the last element in the cache
        if (this.Cache.Count == 1)
        {
            this.LeastRecentlyUsed = this.MostRecentlyUsed = null;
        }
        else if (key.Equals(this.LeastRecentlyUsed.Key))
        {
            Node<K, V> nextLRU = this.LeastRecentlyUsed.Next;
            nextLRU.Previous = null;
            this.LeastRecentlyUsed = nextLRU;
        }
        else if (key.Equals(this.MostRecentlyUsed.Key))
        {
            Node<K, V> nextMRU = this.MostRecentlyUsed.Previous;
            nextMRU.Next = null;
            this.MostRecentlyUsed = nextMRU;
        }
        else
        {
            Node<K, V> nodeToDelete = this.Cache[key];

            Node<K, V> previousNode = nodeToDelete.Previous;
            Node<K, V> nextNode = nodeToDelete.Next;

            previousNode.Next = nextNode;
            nextNode.Previous = previousNode;
        }

        _ = this.Cache.Remove(key);
    }

    public int Count => this.Cache.Count;

    #region IEnumerable
    public IEnumerator<KeyValuePair<K, V>> GetEnumerator()
    {
        Node<K, V> node = this.MostRecentlyUsed;
        while (node != null)
        {
            yield return new KeyValuePair<K, V>(node.Key, node.Value);
            node = node.Previous;
        }
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
    #endregion
}
```
