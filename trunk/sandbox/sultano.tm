<TeXmacs|1.0.6.12>

<style|exam>

<\body>
  <\title>
    Il problema del Sultano
  </title>

  <\exercise>
    Un Sultano deve scegliere la sua nuova moglie tra 100 candidate.

    Il suo interesse è di scegliere la più bella, ma la tradizione vuole che
    lui possa guardare le candidate una sola volta e scegliere la più bella
    senza ripensamenti, fermandosi senza poter guardare le restanti candidate
    e senza poter tornare indietro.

    Presentare una strategia per cui il Sultano riesce nel suo intento con
    una probabilità maggiore del 36%.
  </exercise>

  Prima di affrontare il problema facciamo alcune ipotesi:

  <\itemize-dot>
    <item>Le ragazze sono in ordine casuale di bellezza.

    <item>Le bellezza sono uniche (non esistono due ragazze esattamente
    ``belle'' uguale).

    <item>La bellezza è originata da una probabilità uniforme.
  </itemize-dot>

  Con queste ipotesi, proviamo la strategia di osservare N candidate e poi
  segliere la prima pià bella delle N viste.

  Fissato N:

  <\itemize-arrow>
    <item><math|<frac|N|100>> la 1<rsup|a> più bella è tra le prime N, il
    sultano ha sbagliato

    <item><with|mode|math|<frac|100-N|100>> la 1<rsup|a> più bella è nella
    seconda parte delle ragazze

    <\itemize-arrow>
      <item><strong|<math|<frac|N|100>> la 2<rsup|a> più bella è tra le prime
      N>

      <item><with|mode|math|<frac|100-N|100>> la 2<rsup|a> più bella è nella
      seconda parte delle ragazze

      <\itemize-arrow>
        <item><math|<frac|N|100>> la 3<rsup|a> più bella è tra le prime N

        <\itemize-arrow>
          <item><with|mode|math|<frac|1|2>> 2<rsup|a> \<less\> 1<rsup|a>

          <item><strong|<with|mode|math|<frac|1|2>> 1<rsup|a> \<less\>
          2<rsup|a>>
        </itemize-arrow>

        <item><with|mode|math|<frac|100-N|100>> la 3<rsup|a> più bella è
        nella seconda parte delle ragazze

        <\itemize-arrow>
          <item><math|<frac|N|100>> la 4<rsup|a> più bella è tra le prime N

          <\itemize-arrow>
            <item><with|mode|math|<frac|2|3>> (2<rsup|a>, 3<rsup|a>) \<less\>
            1<rsup|a>

            <item><strong|<with|mode|math|<frac|1|3>> 1<rsup|a> \<less\>
            (2<rsup|a>, 3<rsup|a>)>
          </itemize-arrow>

          <item><with|mode|math|<frac|100-N|100>> la 4<rsup|a> più bella è
          nella seconda parte delle ragazze

          <\itemize-arrow>
            <item>...
          </itemize-arrow>
        </itemize-arrow>
      </itemize-arrow>
    </itemize-arrow>
  </itemize-arrow>

  Possiamo quindi procedere fino ad N e riassumere la probabilità di successo
  con la formula:

  <\equation*>
    P(<with|mode|text|piu-bella>)=<big|sum><rsub|i=1><rsup|N><left|(><frac|100-N|100><right|)><rsup|i>\<cdot\><frac|N|100>\<cdot\><frac|1|i>
  </equation*>

  Con una simulazione possiamo trovare numericamente la probabilità massima
  in funzione di N.

  <with|prog-language|python|prog-session|default|<\session>
    <\input|python] >
      max([(sum([((100-N)/100.)**i * N/100. * 1./i for i in range(1,N+1)]),
      N) for N in range(1,101)])
    </input>

    <\output>
      \ (0.3678733405384419, 37)
    </output>
  </session>>
</body>

<\initial>
  <\collection>
    <associate|language|italian>
  </collection>
</initial>