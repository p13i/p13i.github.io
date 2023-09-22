---
title:
  Design factors for database query domain-specific
  languages (DSLs) in object-oriented languages
categories:
  - research
layout: post
description:
  "Most applications that interface with a database are
  written with object-oriented programming (OOP) languages.
  Many applications use SQL databases to persist data. There
  exists an ‘impedance mismatch’ between the use of
  object-oriented systems that act on objects of non-scalar
  values and the storage of scalar values (e.g. strings and
  integers) organized in SQL tables."
image: "https://github.com/p13i/p13i.github.io/assets/13140065/5ba91cd7-a604-46db-86ad-3209916eff16"
downloads:
  - name: "📜 Report PDF"
    url: https://github.com/p13i/p13i.github.io/files/11621351/2020_11_13._.CS343D._.Essay.Assignment.pdf
---

<!-- Output copied to clipboard! -->

<!-----

Yay, no errors, warnings, or alerts!

Conversion time: 0.734 seconds.


Using this HTML file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β34
* Sun Sep 03 2023 23:55:25 GMT-0700 (PDT)
* Source doc: 2020/11/13 | CS343D | Essay Assignment
* Tables are currently converted to HTML tables.
----->

<p>
<strong>Design factors for database query domain-specific languages (DSLs) in object-oriented languages</strong>
</p>
<p>
<em>Pramod Kotipalli | Stanford CS343D | Fall 2020</em>
</p>
<p>
Most applications that interface with a database are written with object-oriented programming (OOP) languages. <a href="https://scalegrid.io/blog/2019-database-trends-sql-vs-nosql-top-databases-single-vs-multiple-database-use/">Many applications</a> use SQL databases to persist data. There exists an ‘impedance mismatch’ between the use of object-oriented systems that act on objects of non-scalar values and the storage of scalar values (e.g. strings and integers) organized in SQL tables. The ubiquity of OOP systems and SQL databases is hard to overcome; many developers must use both together to write effective and performant web applications. Numerous object-relational mapping (ORM) software libraries exist as libraries for popular languages such as <a href="https://hibernate.org/orm/">Hibernate ORM</a> for Java, <a href="https://guides.rubyonrails.org/active_record_basics.html">Active Record</a> for Ruby, and the <a href="https://docs.djangoproject.com/en/3.1/topics/db/queries/">Django ORM</a> or <a href="https://www.sqlalchemy.org/">SQLAlchemy</a><span style="text-decoration:underline;"> </span>for Python.
</p>
<p>
From the perspective of the programmer of a sophisticated backend API, three language ‘front-end’ design factors are key when selecting or implementing a query DSL for an OOP language (implementation details of ORMs will not be discussed):
</p>
<ol>

<li>Syntax readability

<li>Type-checking

<li>Extensibility
</li>
</ol>
<p>
<strong>Syntax readability</strong>
</p>
<p>
In addition to a method-chaining (i.e. “<a href="https://docs.microsoft.com/en-us/archive/msdn-magazine/2010/january/patterns-in-practice-internal-domain-specific-languages#fluent-interfaces-and-expression-builders">fluent interface</a>”) interface common to many programming languages, some languages have taken to including data querying syntax natively, as in C# with Language Integrated Query (LINQ). This “<a href="https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/">query expression</a>” syntax supports data-query-specific keywords like <code>from </code>and <code>select </code>as native language constructs.
</p>

<table>
  <tr>
   <td colspan="2" ><code>class Person { public int Age; public String Name; }</code>
<p>
<code>Person[] people = new Person[] { </code>
<p>
<code>    new Person { Age = 16, Name = "Alex" }, </code>
<p>
<code>    new Person { Age = 17, Name = "Jamie" }, </code>
<p>
<code>    new Person { Age = 20, Name = "Savannah" } };</code>
   </td>
  </tr>
  <tr>
   <td colspan="2" >Code Fragment 1 - Initializing a <code>people </code>array in C#
   </td>
  </tr>
</table>

<table>
  <tr>
   <td><code>IEnumerable&lt;Person> minors = people.Where(p => p.Age &lt; 18);</code>
<p>
<code>foreach (Person minor in minors) {</code>
<p>
<code>    Console.WriteLine(minor.Name);</code>
<p>
<code>}</code>
   </td>
  </tr>
  <tr>
   <td>Code Fragment 2 - LINQ through a <em>method chaining</em> or a <em>fluent interface </em>syntax
   </td>
  </tr>
</table>

<table>
  <tr>
   <td><code>IEnumerable&lt;Person> minors = from person in people </code>
<p>
<code>    where person.Age &lt; 18 </code>
<p>
<code>    select person;</code>
<p>
<code>foreach (Person minor in minors) {</code>
<p>
<code>    Console.WriteLine(minor.Name);</code>
<p>
<code>}</code>
   </td>
  </tr>
  <tr>
   <td>Code Fragment 3 - LINQ through <em>query expression </em>syntax
   </td>
  </tr>
</table>

<p>
Note that both the method chaining and query expression approaches yield the same <code>IEnumerable</code> collection type: both approaches are semantically equivalent. However, some queries are more readable in one form over another. Some developers may even take the approach of using the query expression syntax for database queries and the fluent interface for in-memory collection manipulation. Therefore, supporting multiple query syntaxes is one important factor for when selecting the enclosing programming language.
</p>
<p>
Further, the support of syntactically-simple lambda expressions is crucial for readable queries. This is a feature that popular languages like Python do not support. An equivalent to Code Fragment 2 with Python lambdas would print as: 
</p>

<table>
  <tr>
   <td><code>minors = Person.objects.filter(lambda p: p.Age &lt; 18)</code>
   </td>
  </tr>
  <tr>
   <td>Code Fragment 4 - Python lambda syntax in an ORM query
   </td>
  </tr>
</table>

<p>
The use of the <code>lambda</code> keyword over the <code>=></code> in more sophisticated queries grows to be a tiresome syntax.
</p>
<p>
<strong>Type-checking</strong>
</p>
<p>
C#’s support of LINQ enables compile-time type checking of every query written in a program. Django’s ORM is constrained to Python’s dynamic type checking system leading to syntax like so for a similar C# query.
</p>

<table>
  <tr>
   <td><code>minors = Person.object.filter(age__lt=18)</code>
<p>
<code>for minor in minors:</code>
<p>
<code>   print(minor.Name)</code>
   </td>
  </tr>
  <tr>
   <td>Code Fragment 5 - A query for <code>minors </code>through a Python ORM
   </td>
  </tr>
</table>

<p>
Note that Python-based ORMs must rely on method-chaining syntax, straying one level of abstraction away from the SQL-like syntax of C# query expressions. Also note the <code>age__lt=18</code> argument to the <code>filter</code> method; such methods (e.g. <code>lte </code>for <code>&lt;=</code>, <code>gt</code>, <code>gte</code>, <code>in</code>, <code>contains</code>, <a href="https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4">etc.</a>) are programmatically-generated by Django for each property of a database object. The limitations of Python’s dynamic typing system means that Django must take arguments of the <code>filter</code> method, parse it (e.g. as <code>age </code>and <code>lt</code> for the <code>&lt;</code> operator) and then evaluate its semantics before generating SQL, all adding additional overhead to the program’s runtime without the benefits of compile-time type-checking.
</p>
<p>
As the complexity of object-oriented systems grows, developers tend to write less and less tests (if any to begin with) making the importance of compile-time type checking more important. Pre-deployment compilation or type-checking is an important factor for the selection of a programming language for an ORM, either for a programmer or an ORM implementor. Python’s best approach to this problem is using an optional static type checker, <a href="http://mypy-lang.org/">mypy</a>, which can check a Python program before it is deployed. However, mypy is not able to actually compile and optimize code as with statically-typed languages.
</p>
<p>
C# also supports statically-typed <a href="https://docs.microsoft.com/en-us/dotnet/standard/linq/project-anonymous-type">anonymous types</a> enabling C# to represent intermediate query results in simple struct-like types without adding code bloat from an additional declaration.
</p>
<p>
<strong>Extensibility</strong>
</p>
<p>
C#’s support of extension methods is extremely useful for both readability and keeping code DRY. Take for example <a href="https://docs.microsoft.com/en-us/archive/msdn-magazine/2010/january/patterns-in-practice-internal-domain-specific-languages">the expression of a time-difference object</a>. To express a time delta of 30 days, we can write <code>new TimeSpan(30, 0, 0, 0)</code>. An experienced programmer can read this as “30 days, 0 hours, 0 minutes, and 0 seconds” but even for such programmers using the <code>new TimeSpan </code>syntax can get quite tiresome. C# supports extension methods which form syntactic sugar for method chaining, a much more readable form:
</p>

<table>
  <tr>
   <td><code>public static class DateTimeExtensions</code>
<p>
<code>{</code>
<p>
<code>    public static TimeSpan Days(this int number)</code>
<p>
<code>    {</code>
<p>
<code>        return new TimeSpan(number, 0, 0, 0);</code>
<p>
<code>    }</code>
<p>
<code>}</code>
<p>
<code>...</code>
<p>
<code>30.Days(); // Equivalent to new Timespan(30, 0, 0, 0);</code>
   </td>
  </tr>
  <tr>
   <td>Code Fragment 6 - “<a href="https://docs.microsoft.com/en-us/archive/msdn-magazine/2010/january/patterns-in-practice-internal-domain-specific-languages#literal-extensions">Literal expressions</a>” in C#
   </td>
  </tr>
</table>

<p>
This form of language augmentability supports the creation of DSLs for domains further than that of generic database queries. We can now support method chaining that makes sense for a particular domain, such as for an API managing a store: <code>user.GetOrders().Where(order => order.DaysOnShelf &lt; 3.Days());</code>. If we need to access such orders multiple times, we can simply declare a reusable extension method that encodes this lambda:
</p>

<table>
  <tr>
   <td><code>public static class OrderExtensions</code>
<p>
<code>{</code>
<p>
<code>    public static IEnumerable&lt;Order> OnShelfForShortTime(</code>
<p>
<code>        this IEnumerable&lt;Order> orders)</code>
<p>
<code>    {</code>
<p>
<code>        return orders.Where(order => </code>
<p>
<code>            order.DaysOnShelf &lt; 3.Days());</code>
<p>
<code>    }</code>
<p>
<code>}</code>
<p>
<code>...</code>
<p>
<code>user.GetOrders().OnShelfForShortTime(); // Equivalent form</code>
   </td>
  </tr>
  <tr>
   <td>Code Fragment 7 - “<a href="https://docs.microsoft.com/en-us/archive/msdn-magazine/2010/january/patterns-in-practice-internal-domain-specific-languages#literal-extensions">Literal expressions</a>” in C#
   </td>
  </tr>
</table>

<p>
With extensibility, query syntax is easier to read and lends itself to DRY implementations of large systems. While other ORMs support such augmentations, they are usually implemented through proxy objects or by utilizing the dynamically-typed nature of languages.
</p>
<p>
<strong>Final thoughts</strong>
</p>
<p>
While this essay may seem like a document exalting the expressiveness and simplicity of LINQ, I try to show that some core language features of C# are very useful for interacting with data through ORMs and creating DSLs for data queries. The support of native language query expressions and extension methods provide for readability and extensibility. The statically-typed nature of C# provides the programmer with many assurances during development. Many ORMs and data-interfacing query languages in OOP contexts can benefit from supporting C#-like language features.
</p>
