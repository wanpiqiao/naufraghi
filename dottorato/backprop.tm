<TeXmacs|1.0.6.12>

<style|article>

<\body>
  <doc-data|<doc-title|Backprop>|<\doc-author-data|<author-name|Matteo
  Bertini>>
    \;
  </doc-author-data|<\author-address>
    matteo@naufraghi.net
  </author-address>>|<\doc-date>
    <date>
  </doc-date>>

  <section|Feed Forward>

  <big-figure|<postscript|backprop.eps|*3/5|*3/5||||>|Layer>

  Per ogni layer da quello i input a quello di output:

  <\equation*>
    layer<rsub|i+1>.input=layer<rsub|i>.output
  </equation*>

  Per ogni <math|k> in <math|outputs>:

  <\eqnarray*>
    <tformat|<table|<row|<cell|<with|math-font-series|bold|output>[k]>|<cell|=
    >|<cell|squash<left|(><big|sum><rsub|j=0><rsup|len(<with|math-font-series|bold|inputs>)><with|math-font-series|bold|weights[k]>[j]\<cdot\><with|math-font-series|bold|inputs>[j]<right|)>=>>|<row|<cell|>|<cell|=>|<cell|squash<left|(>dot(<with|math-font-series|bold|weights[k]>,
    <with|math-font-series|bold|inputs>)<right|)>>>>>
  </eqnarray*>

  \;

  \;

  \;
</body>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|?>>
    <associate|auto-2|<tuple|1|?>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|figure>
      <tuple|normal|Layer|<pageref|auto-2>>
    </associate>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Feed
      Forward> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>