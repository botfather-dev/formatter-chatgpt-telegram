from chatgpt_md_converter.html_splitter import split_html_for_telegram

input_text ="""


Absolutely! Here’s a Markdown-formatted message exceeding 5,000 characters, exploring <b>The History and Impact of Computer Programming</b>. (You can verify the character count using any online tool.)

---

<b>The History and Impact of Computer Programming</b>

<i>“The computer was born to solve problems that did not exist before.”</i>  
— Bill Gates

---

<b>Table of Contents</b>

1. <a href="#introduction">Introduction</a>  
2. <a href="#ancient-beginnings-from-algorithms-to-machines">Ancient Beginnings: From Algorithms to Machines</a>  
    • <a href="#al-khwarizmi-and-the-algorithm">Al-Khwarizmi and the Algorithm</a>  
    • <a href="#the-analytical-engine">The Analytical Engine</a>  
    • <a href="#punch-cards-and-the-jacquard-loom">Punch Cards and the Jacquard Loom</a>  
3. <a href="#20th-century-the-birth-of-modern-programming">20th Century: The Birth of Modern Programming</a>  
    • <a href="#eniac-and-early-programmers">ENIAC and Early Programmers</a>  
    • <a href="#assembly-language-and-early-high-level-languages">Assembly Language and Early High-level Languages</a>  
    • <a href="#cobol-fortran-and-the-expansion">COBOL, FORTRAN, and the Expansion</a>  
4. <a href="#modern-era-languages-paradigms-and-the-internet">Modern Era: Languages, Paradigms, and the Internet</a>  
    • <a href="#object-oriented-programming">Object-Oriented Programming</a>  
    • <a href="#internet-and-open-source">Internet and Open Source</a>  
    • <a href="#mobile-and-cloud-computing">Mobile and Cloud Computing</a>    
5. <a href="#programmings-societal-impact">Programming’s Societal Impact</a>  
6. <a href="#ethics-challenges-and-the-future">Ethics, Challenges, and the Future</a>  
7. <a href="#conclusion">Conclusion</a>  
8. <a href="#useful-resources">Useful Resources</a>  

---

<b>Introduction</b>

Computer programming is the science and art of giving computers instructions to perform specific tasks. Today, it's impossible to imagine a world without software: from banking systems and mobile applications to traffic lights and airplanes, programming is everywhere.

But how did programming begin, and what has it become today? This document explores the journey of programming, from ancient mathematical roots to the future of artificial intelligence.

---

<b>Ancient Beginnings: From Algorithms to Machines</b>

<b>Al-Khwarizmi and the Algorithm</b>

The term "<b>algorithm</b>" (the foundation of programming) comes from Abu Abdullah Muhammad ibn Musa Al-Khwarizmi, a 9th-century Persian mathematician. His works on systematic procedures laid the groundwork for computational thinking.

<b>The Analytical Engine</b>

In the 19th century, <b>Charles Babbage</b> designed the Analytical Engine, a mechanical general-purpose computer. Though never built in his lifetime, it could—in theory—read instructions from punched cards.

<b>Ada Lovelace</b>, Babbage's collaborator, is often called the first computer programmer. She wrote notes describing algorithms (in essence, programs) for the Analytical Engine to compute Bernoulli numbers.

<blockquote>"That brain of mine is something more than merely mortal; as time will show."
– Ada Lovelace</blockquote>

<b>Punch Cards and the Jacquard Loom</b>

The concept of programming a machine with punched cards predates computers. <b>Joseph Marie Jacquard</b> invented a loom in 1804 that used punched cards to control patterns in woven fabric—an early example of machine automation.

---

<b>20th Century: The Birth of Modern Programming</b>

<b>ENIAC and Early Programmers</b>

ENIAC (Electronic Numerical Integrator and Computer), completed in 1945, is often cited as the first electronic general-purpose computer.

Early programming was entirely manual and physically laborious—think patch cables and switches!

Notably, many of the earliest programmers were women, such as <b>Kathleen McNulty</b>, <b>Jean Jennings</b>, and <b>Grace Hopper</b>.

<b>Assembly Language and Early High-level Languages</b>

The problem of complexity led to <b>assembly languages</b>, where mnemonics like <code>MOV</code> and <code>ADD</code> replaced binary codes. Programming became more accessible, but code was still hardware-specific.

The 1950s saw the creation of:

• <b>FORTRAN</b> (FORmula TRANslation) for scientific computation
• <b>COBOL</b> (COmmon Business-Oriented Language) for business applications

<b>Code Example: Hello World in COBOL</b>
<pre><code class="language-cobol">IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO-WORLD.
PROCEDURE DIVISION.
    DISPLAY "Hello, World!".
STOP RUN.
</code></pre>

<b>COBOL, FORTRAN, and the Expansion</b>

With the advent of high-level languages, programming became less about circuitry and more about solving problems. Standardized languages allowed code to run on multiple machines.

Other languages soon emerged:

• <b>LISP</b> (for AI research)
• <b>ALGOL</b> (basis for many future languages)
• <b>BASIC</b> (for beginners and education)

---

<b>Modern Era: Languages, Paradigms, and the Internet</b>

<b>Object-Oriented Programming</b>

The 1970s and 1980s introduced <b>object-oriented programming</b> (OOP), where data and behavior are bundled together. The most influential languages here include:

• <b>Smalltalk</b>: pioneered OOP concepts
• <b>C++</b>: combined OOP with the efficiency of C
• <b>Java</b>: “Write Once, Run Anywhere” with the Java Virtual Machine

<b>Code Example: Simple Class in Java</b>
<pre><code class="language-java">public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
</code></pre>

<b>Internet and Open Source</b>

The rise of the World Wide Web transformed programming. JavaScript, PHP, and Python became staples for Internet-connected software.

<b>Open source</b> projects like Linux, Apache, and MySQL changed collaboration forever—developers worldwide could contribute to shared codebases.

| Year | Technology  | Impact                                  |
|------|-------------|-----------------------------------------|
| 1991 | Linux       | Free, open-source operating systems     |
| 1995 | JavaScript  | Interactive web applications            |
| 2001 | Wikipedia   | Collaborative knowledge base            |

<b>Mobile and Cloud Computing</b>

Smartphones spawned new languages and frameworks (Swift, Kotlin, React Native).

<b>Cloud computing</b> and <b>APIs</b> mean programs can collaborate on a global scale, in real-time.

---

<b>Programming’s Societal Impact</b>

Programming is reshaping society in profound ways:

• <b>Healthcare</b>: Medical imaging, diagnostics, record management
• <b>Finance</b>: Online banking, stock trading algorithms
• <b>Entertainment</b>: Gaming, music streaming, social networks
• <b>Education</b>: E-learning, interactive simulations, content platforms
• <b>Transportation</b>: Navigation, ride-sharing apps, autonomous vehicles
• <b>Science</b>: Processing large datasets, running complex simulations

<blockquote>“Software is eating the world.”
– Marc Andreessen</blockquote>

<b>Programming Jobs In Demand</b>

<pre><code class="language-mermaid">pie
    title Programming Job Market (2024)
    "Web Development" : 31
    "Data Science" : 22
    "Mobile Development" : 12
    "Embedded Systems" : 8
    "Cybersecurity" : 9
    "Other": 18
</code></pre>

<b>Note:</b> Mermaid diagrams require compatible renderers (e.g., GitHub, Obsidian).

---

<b>Ethics, Challenges, and the Future</b>

With great power comes responsibility. Programmers face new challenges:

• <b>Bias in Algorithms:</b> Unintentional biases in data can lead to unfair outcomes (e.g., in hiring software or criminal justice prediction).
• <b>Privacy:</b> Handling personal data securely is more critical than ever.
• <b>Safety:</b> In fields like self-driving cars or medical devices, software bugs can have real-world consequences.
• <b>Sustainability:</b> Software should be efficient, minimizing environmental impact in data centers.

<b>Emerging Trends:</b>

• <b>Artificial Intelligence:</b> Programs that learn, adapt, and sometimes surprise their creators.
• <b>Quantum Computing:</b> New paradigms for solving currently intractable problems.
• <b>No-Code/Low-Code:</b> Empowering more people to harness computational power.

---

<b>Conclusion</b>

From mechanical looms to neural networks, programming continues to redefine what’s possible. It’s not just for professional engineers: millions of people use programming as a tool for art, science, business, and personal growth.

<b>Everyone can learn to code.</b> It might change your life—or even the world.

<blockquote>"Any sufficiently advanced technology is indistinguishable from magic."
— Arthur C. Clarke</blockquote>

---

<b>Useful Resources</b>

• <a href="https://www-cs-faculty.stanford.edu/~knuth/taocp.html">The Art of Computer Programming (Donald Knuth)</a>
• <a href="https://www.khanacademy.org/computing/computer-programming">Khan Academy Computer Programming</a>
• <a href="https://www.w3schools.com/">W3Schools Online Tutorials</a>
• <a href="https://www.freecodecamp.org/">freeCodeCamp</a>
• <a href="https://stackoverflow.com/">Stack Overflow</a>
• <a href="https://guides.github.com/">GitHub Guides</a>

---

<i>Thank you for reading! If you’re inspired to begin your coding journey, there has never been a better time to start.</i>

---"""

valid_chunk_1 = """


Absolutely! Here’s a Markdown-formatted message exceeding 5,000 characters, exploring <b>The History and Impact of Computer Programming</b>. (You can verify the character count using any online tool.)

---

<b>The History and Impact of Computer Programming</b>

<i>“The computer was born to solve problems that did not exist before.”</i>  
— Bill Gates

---

<b>Table of Contents</b>

1. <a href="#introduction">Introduction</a>  
2. <a href="#ancient-beginnings-from-algorithms-to-machines">Ancient Beginnings: From Algorithms to Machines</a>  
    • <a href="#al-khwarizmi-and-the-algorithm">Al-Khwarizmi and the Algorithm</a>  
    • <a href="#the-analytical-engine">The Analytical Engine</a>  
    • <a href="#punch-cards-and-the-jacquard-loom">Punch Cards and the Jacquard Loom</a>  
3. <a href="#20th-century-the-birth-of-modern-programming">20th Century: The Birth of Modern Programming</a>  
    • <a href="#eniac-and-early-programmers">ENIAC and Early Programmers</a>  
    • <a href="#assembly-language-and-early-high-level-languages">Assembly Language and Early High-level Languages</a>  
    • <a href="#cobol-fortran-and-the-expansion">COBOL, FORTRAN, and the Expansion</a>  
4. <a href="#modern-era-languages-paradigms-and-the-internet">Modern Era: Languages, Paradigms, and the Internet</a>  
    • <a href="#object-oriented-programming">Object-Oriented Programming</a>  
    • <a href="#internet-and-open-source">Internet and Open Source</a>  
    • <a href="#mobile-and-cloud-computing">Mobile and Cloud Computing</a>    
5. <a href="#programmings-societal-impact">Programming’s Societal Impact</a>  
6. <a href="#ethics-challenges-and-the-future">Ethics, Challenges, and the Future</a>  
7. <a href="#conclusion">Conclusion</a>  
8. <a href="#useful-resources">Useful Resources</a>  

---

<b>Introduction</b>

Computer programming is the science and art of giving computers instructions to perform specific tasks. Today, it's impossible to imagine a world without software: from banking systems and mobile applications to traffic lights and airplanes, programming is everywhere.

But how did programming begin, and what has it become today? This document explores the journey of programming, from ancient mathematical roots to the future of artificial intelligence.

---

<b>Ancient Beginnings: From Algorithms to Machines</b>

<b>Al-Khwarizmi and the Algorithm</b>

The term "<b>algorithm</b>" (the foundation of programming) comes from Abu Abdullah Muhammad ibn Musa Al-Khwarizmi, a 9th-century Persian mathematician. His works on systematic procedures laid the groundwork for computational thinking.

<b>The Analytical Engine</b>

In the 19th century, <b>Charles Babbage</b> designed the Analytical Engine, a mechanical general-purpose computer. Though never built in his lifetime, it could—in theory—read instructions from punched cards.

<b>Ada Lovelace</b>, Babbage's collaborator, is often called the first computer programmer. She wrote notes describing algorithms (in essence, programs) for the Analytical Engine to compute Bernoulli numbers.

<blockquote>"That brain of mine is something more than merely mortal; as time will show."
– Ada Lovelace</blockquote>

<b>Punch Cards and the Jacquard Loom</b>

The concept of programming a machine with punched cards predates computers. <b>Joseph Marie Jacquard</b> invented a loom in 1804 that used punched cards to control patterns in woven fabric—an early example of machine automation.

---

<b>20th Century: The Birth of Modern Programming</b>

<b>ENIAC and Early Programmers</b>

ENIAC (Electronic Numerical Integrator and Computer), completed in 1945, is often cited as the first electronic general-purpose computer.

Early programming was entirely manual and physically laborious—think patch cables and switches!

Notably, many of the earliest programmers were women, such as <b>Kathleen McNulty</b>, <b>Jean Jennings</b>, and <b>Grace Hopper</b>.

<b>Assembly Language and Early High-level Languages</b>

"""

valid_chunk_2 = """The problem of complexity led to <b>assembly languages</b>, where mnemonics like <code>MOV</code> and <code>ADD</code> replaced binary codes. Programming became more accessible, but code was still hardware-specific.

The 1950s saw the creation of:

• <b>FORTRAN</b> (FORmula TRANslation) for scientific computation
• <b>COBOL</b> (COmmon Business-Oriented Language) for business applications

<b>Code Example: Hello World in COBOL</b>
<pre><code class="language-cobol">IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO-WORLD.
PROCEDURE DIVISION.
    DISPLAY "Hello, World!".
STOP RUN.
</code></pre>

<b>COBOL, FORTRAN, and the Expansion</b>

With the advent of high-level languages, programming became less about circuitry and more about solving problems. Standardized languages allowed code to run on multiple machines.

Other languages soon emerged:

• <b>LISP</b> (for AI research)
• <b>ALGOL</b> (basis for many future languages)
• <b>BASIC</b> (for beginners and education)

---

<b>Modern Era: Languages, Paradigms, and the Internet</b>

<b>Object-Oriented Programming</b>

The 1970s and 1980s introduced <b>object-oriented programming</b> (OOP), where data and behavior are bundled together. The most influential languages here include:

• <b>Smalltalk</b>: pioneered OOP concepts
• <b>C++</b>: combined OOP with the efficiency of C
• <b>Java</b>: “Write Once, Run Anywhere” with the Java Virtual Machine

<b>Code Example: Simple Class in Java</b>
<pre><code class="language-java">public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
</code></pre>

<b>Internet and Open Source</b>

The rise of the World Wide Web transformed programming. JavaScript, PHP, and Python became staples for Internet-connected software.

<b>Open source</b> projects like Linux, Apache, and MySQL changed collaboration forever—developers worldwide could contribute to shared codebases.

| Year | Technology  | Impact                                  |
|------|-------------|-----------------------------------------|
| 1991 | Linux       | Free, open-source operating systems     |
| 1995 | JavaScript  | Interactive web applications            |
| 2001 | Wikipedia   | Collaborative knowledge base            |

<b>Mobile and Cloud Computing</b>

Smartphones spawned new languages and frameworks (Swift, Kotlin, React Native).

<b>Cloud computing</b> and <b>APIs</b> mean programs can collaborate on a global scale, in real-time.

---

<b>Programming’s Societal Impact</b>

Programming is reshaping society in profound ways:

• <b>Healthcare</b>: Medical imaging, diagnostics, record management
• <b>Finance</b>: Online banking, stock trading algorithms
• <b>Entertainment</b>: Gaming, music streaming, social networks
• <b>Education</b>: E-learning, interactive simulations, content platforms
• <b>Transportation</b>: Navigation, ride-sharing apps, autonomous vehicles
• <b>Science</b>: Processing large datasets, running complex simulations

<blockquote>“Software is eating the world.”
– Marc Andreessen</blockquote>

<b>Programming Jobs In Demand</b>

<pre><code class="language-mermaid">pie
    title Programming Job Market (2024)
    "Web Development" : 31
    "Data Science" : 22
    "Mobile Development" : 12
    "Embedded Systems" : 8
    "Cybersecurity" : 9
    "Other": 18
</code></pre>"""

valid_chunk_3 = """

<b>Note:</b> Mermaid diagrams require compatible renderers (e.g., GitHub, Obsidian).

---

<b>Ethics, Challenges, and the Future</b>

With great power comes responsibility. Programmers face new challenges:

• <b>Bias in Algorithms:</b> Unintentional biases in data can lead to unfair outcomes (e.g., in hiring software or criminal justice prediction).
• <b>Privacy:</b> Handling personal data securely is more critical than ever.
• <b>Safety:</b> In fields like self-driving cars or medical devices, software bugs can have real-world consequences.
• <b>Sustainability:</b> Software should be efficient, minimizing environmental impact in data centers.

<b>Emerging Trends:</b>

• <b>Artificial Intelligence:</b> Programs that learn, adapt, and sometimes surprise their creators.
• <b>Quantum Computing:</b> New paradigms for solving currently intractable problems.
• <b>No-Code/Low-Code:</b> Empowering more people to harness computational power.

---

<b>Conclusion</b>

From mechanical looms to neural networks, programming continues to redefine what’s possible. It’s not just for professional engineers: millions of people use programming as a tool for art, science, business, and personal growth.

<b>Everyone can learn to code.</b> It might change your life—or even the world.

<blockquote>"Any sufficiently advanced technology is indistinguishable from magic."
— Arthur C. Clarke</blockquote>

---

<b>Useful Resources</b>

• <a href="https://www-cs-faculty.stanford.edu/~knuth/taocp.html">The Art of Computer Programming (Donald Knuth)</a>
• <a href="https://www.khanacademy.org/computing/computer-programming">Khan Academy Computer Programming</a>
• <a href="https://www.w3schools.com/">W3Schools Online Tutorials</a>
• <a href="https://www.freecodecamp.org/">freeCodeCamp</a>
• <a href="https://stackoverflow.com/">Stack Overflow</a>
• <a href="https://guides.github.com/">GitHub Guides</a>

---

<i>Thank you for reading! If you’re inspired to begin your coding journey, there has never been a better time to start.</i>

---"""

def test_html_splitter():
  chunks = split_html_for_telegram(input_text)
  valid_chunks = [valid_chunk_1, valid_chunk_2, valid_chunk_3]
  for index, valid_chunk in enumerate(valid_chunks):
    assert chunks[index] == valid_chunk

valid_chunk_1_remove_leading_brakes = """Absolutely! Here’s a Markdown-formatted message exceeding 5,000 characters, exploring <b>The History and Impact of Computer Programming</b>. (You can verify the character count using any online tool.)

---

<b>The History and Impact of Computer Programming</b>

<i>“The computer was born to solve problems that did not exist before.”</i>  
— Bill Gates

---

<b>Table of Contents</b>

1. <a href="#introduction">Introduction</a>  
2. <a href="#ancient-beginnings-from-algorithms-to-machines">Ancient Beginnings: From Algorithms to Machines</a>  
    • <a href="#al-khwarizmi-and-the-algorithm">Al-Khwarizmi and the Algorithm</a>  
    • <a href="#the-analytical-engine">The Analytical Engine</a>  
    • <a href="#punch-cards-and-the-jacquard-loom">Punch Cards and the Jacquard Loom</a>  
3. <a href="#20th-century-the-birth-of-modern-programming">20th Century: The Birth of Modern Programming</a>  
    • <a href="#eniac-and-early-programmers">ENIAC and Early Programmers</a>  
    • <a href="#assembly-language-and-early-high-level-languages">Assembly Language and Early High-level Languages</a>  
    • <a href="#cobol-fortran-and-the-expansion">COBOL, FORTRAN, and the Expansion</a>  
4. <a href="#modern-era-languages-paradigms-and-the-internet">Modern Era: Languages, Paradigms, and the Internet</a>  
    • <a href="#object-oriented-programming">Object-Oriented Programming</a>  
    • <a href="#internet-and-open-source">Internet and Open Source</a>  
    • <a href="#mobile-and-cloud-computing">Mobile and Cloud Computing</a>    
5. <a href="#programmings-societal-impact">Programming’s Societal Impact</a>  
6. <a href="#ethics-challenges-and-the-future">Ethics, Challenges, and the Future</a>  
7. <a href="#conclusion">Conclusion</a>  
8. <a href="#useful-resources">Useful Resources</a>  

---

<b>Introduction</b>

Computer programming is the science and art of giving computers instructions to perform specific tasks. Today, it's impossible to imagine a world without software: from banking systems and mobile applications to traffic lights and airplanes, programming is everywhere.

But how did programming begin, and what has it become today? This document explores the journey of programming, from ancient mathematical roots to the future of artificial intelligence.

---

<b>Ancient Beginnings: From Algorithms to Machines</b>

<b>Al-Khwarizmi and the Algorithm</b>

The term "<b>algorithm</b>" (the foundation of programming) comes from Abu Abdullah Muhammad ibn Musa Al-Khwarizmi, a 9th-century Persian mathematician. His works on systematic procedures laid the groundwork for computational thinking.

<b>The Analytical Engine</b>

In the 19th century, <b>Charles Babbage</b> designed the Analytical Engine, a mechanical general-purpose computer. Though never built in his lifetime, it could—in theory—read instructions from punched cards.

<b>Ada Lovelace</b>, Babbage's collaborator, is often called the first computer programmer. She wrote notes describing algorithms (in essence, programs) for the Analytical Engine to compute Bernoulli numbers.

<blockquote>"That brain of mine is something more than merely mortal; as time will show."
– Ada Lovelace</blockquote>

<b>Punch Cards and the Jacquard Loom</b>

The concept of programming a machine with punched cards predates computers. <b>Joseph Marie Jacquard</b> invented a loom in 1804 that used punched cards to control patterns in woven fabric—an early example of machine automation.

---

<b>20th Century: The Birth of Modern Programming</b>

<b>ENIAC and Early Programmers</b>

ENIAC (Electronic Numerical Integrator and Computer), completed in 1945, is often cited as the first electronic general-purpose computer.

Early programming was entirely manual and physically laborious—think patch cables and switches!

Notably, many of the earliest programmers were women, such as <b>Kathleen McNulty</b>, <b>Jean Jennings</b>, and <b>Grace Hopper</b>.

<b>Assembly Language and Early High-level Languages</b>

"""

valid_chunk_2_remove_leading_brakes = """The problem of complexity led to <b>assembly languages</b>, where mnemonics like <code>MOV</code> and <code>ADD</code> replaced binary codes. Programming became more accessible, but code was still hardware-specific.

The 1950s saw the creation of:

• <b>FORTRAN</b> (FORmula TRANslation) for scientific computation
• <b>COBOL</b> (COmmon Business-Oriented Language) for business applications

<b>Code Example: Hello World in COBOL</b>
<pre><code class="language-cobol">IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO-WORLD.
PROCEDURE DIVISION.
    DISPLAY "Hello, World!".
STOP RUN.
</code></pre>

<b>COBOL, FORTRAN, and the Expansion</b>

With the advent of high-level languages, programming became less about circuitry and more about solving problems. Standardized languages allowed code to run on multiple machines.

Other languages soon emerged:

• <b>LISP</b> (for AI research)
• <b>ALGOL</b> (basis for many future languages)
• <b>BASIC</b> (for beginners and education)

---

<b>Modern Era: Languages, Paradigms, and the Internet</b>

<b>Object-Oriented Programming</b>

The 1970s and 1980s introduced <b>object-oriented programming</b> (OOP), where data and behavior are bundled together. The most influential languages here include:

• <b>Smalltalk</b>: pioneered OOP concepts
• <b>C++</b>: combined OOP with the efficiency of C
• <b>Java</b>: “Write Once, Run Anywhere” with the Java Virtual Machine

<b>Code Example: Simple Class in Java</b>
<pre><code class="language-java">public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
</code></pre>

<b>Internet and Open Source</b>

The rise of the World Wide Web transformed programming. JavaScript, PHP, and Python became staples for Internet-connected software.

<b>Open source</b> projects like Linux, Apache, and MySQL changed collaboration forever—developers worldwide could contribute to shared codebases.

| Year | Technology  | Impact                                  |
|------|-------------|-----------------------------------------|
| 1991 | Linux       | Free, open-source operating systems     |
| 1995 | JavaScript  | Interactive web applications            |
| 2001 | Wikipedia   | Collaborative knowledge base            |

<b>Mobile and Cloud Computing</b>

Smartphones spawned new languages and frameworks (Swift, Kotlin, React Native).

<b>Cloud computing</b> and <b>APIs</b> mean programs can collaborate on a global scale, in real-time.

---

<b>Programming’s Societal Impact</b>

Programming is reshaping society in profound ways:

• <b>Healthcare</b>: Medical imaging, diagnostics, record management
• <b>Finance</b>: Online banking, stock trading algorithms
• <b>Entertainment</b>: Gaming, music streaming, social networks
• <b>Education</b>: E-learning, interactive simulations, content platforms
• <b>Transportation</b>: Navigation, ride-sharing apps, autonomous vehicles
• <b>Science</b>: Processing large datasets, running complex simulations

<blockquote>“Software is eating the world.”
– Marc Andreessen</blockquote>

<b>Programming Jobs In Demand</b>

<pre><code class="language-mermaid">pie
    title Programming Job Market (2024)
    "Web Development" : 31
    "Data Science" : 22
    "Mobile Development" : 12
    "Embedded Systems" : 8
    "Cybersecurity" : 9
    "Other": 18
</code></pre>"""

valid_chunk_3_remove_leading_brakes = """<b>Note:</b> Mermaid diagrams require compatible renderers (e.g., GitHub, Obsidian).

---

<b>Ethics, Challenges, and the Future</b>

With great power comes responsibility. Programmers face new challenges:

• <b>Bias in Algorithms:</b> Unintentional biases in data can lead to unfair outcomes (e.g., in hiring software or criminal justice prediction).
• <b>Privacy:</b> Handling personal data securely is more critical than ever.
• <b>Safety:</b> In fields like self-driving cars or medical devices, software bugs can have real-world consequences.
• <b>Sustainability:</b> Software should be efficient, minimizing environmental impact in data centers.

<b>Emerging Trends:</b>

• <b>Artificial Intelligence:</b> Programs that learn, adapt, and sometimes surprise their creators.
• <b>Quantum Computing:</b> New paradigms for solving currently intractable problems.
• <b>No-Code/Low-Code:</b> Empowering more people to harness computational power.

---

<b>Conclusion</b>

From mechanical looms to neural networks, programming continues to redefine what’s possible. It’s not just for professional engineers: millions of people use programming as a tool for art, science, business, and personal growth.

<b>Everyone can learn to code.</b> It might change your life—or even the world.

<blockquote>"Any sufficiently advanced technology is indistinguishable from magic."
— Arthur C. Clarke</blockquote>

---

<b>Useful Resources</b>

• <a href="https://www-cs-faculty.stanford.edu/~knuth/taocp.html">The Art of Computer Programming (Donald Knuth)</a>
• <a href="https://www.khanacademy.org/computing/computer-programming">Khan Academy Computer Programming</a>
• <a href="https://www.w3schools.com/">W3Schools Online Tutorials</a>
• <a href="https://www.freecodecamp.org/">freeCodeCamp</a>
• <a href="https://stackoverflow.com/">Stack Overflow</a>
• <a href="https://guides.github.com/">GitHub Guides</a>

---

<i>Thank you for reading! If you’re inspired to begin your coding journey, there has never been a better time to start.</i>

---"""

def test_html_splitter__remove_leading_brakes():
  chunks = split_html_for_telegram(input_text, 
                                   trim_leading_newlines=True)
  valid_chunks = [valid_chunk_1_remove_leading_brakes, valid_chunk_2_remove_leading_brakes, valid_chunk_3_remove_leading_brakes]
  for index, valid_chunk in enumerate(valid_chunks):
    assert chunks[index] == valid_chunk