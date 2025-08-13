# GUIÓN DE LLAMADA - SERVICIO DE PREVENCIÓN DE FRAUDES
## BANCO SANTANDER - DURACIÓN APROXIMADA: 60 MINUTOS

---

### INICIO DE LA LLAMADA (Minutos 0-5)

**[Tono de llamada]**

**AGENTE:** Buenos días, ¿hablo con doña Alicia García?

**CLIENTE:** Sí, soy yo.

**AGENTE:** Muy buenos días, doña Alicia. Mi nombre es Carlos Rodríguez Martínez, y le llamo desde el Servicio de Prevención de Fraudes del Banco Santander. Antes de continuar, debo informarle que esta llamada está siendo grabada por razones legales y de seguridad, de acuerdo con la normativa vigente de protección de datos y prevención del blanqueo de capitales. ¿Le parece bien que continuemos?

**CLIENTE:** Sí, claro, pero... ¿ha pasado algo con mi cuenta?

**AGENTE:** Efectivamente, doña Alicia, por eso me pongo en contacto con usted esta mañana. Hemos detectado una actividad inusual en su cuenta que requiere su atención inmediata. Pero antes de entrar en detalles, necesito confirmar que está usted en un lugar donde pueda hablar con tranquilidad durante unos minutos. Esta conversación es importante y necesitaré su total atención.

**CLIENTE:** Sí, estoy en casa. Puedo hablar.

**AGENTE:** Perfecto. Doña Alicia, ¿tendría a mano su teléfono móvil con la aplicación del Banco Santander instalada? O si lo prefiere, ¿tiene acceso a su banca online desde un ordenador? Es posible que necesitemos validar algunos datos durante nuestra conversación.

**CLIENTE:** Sí, tengo aquí mi móvil con la aplicación.

**AGENTE:** Excelente, doña Alicia. Manténgalo cerca por si lo necesitamos. Antes de continuar, y por protocolo de seguridad, necesito verificar algunos datos con usted. ¿Podría confirmarme los últimos cuatro dígitos de su DNI?

**CLIENTE:** Claro, son 4567.

**AGENTE:** Correcto. Y por favor, ¿podría indicarme su fecha de nacimiento?

**CLIENTE:** 15 de marzo de 1975.

**AGENTE:** Perfecto, muchas gracias. Doña Alicia, ahora que hemos verificado su identidad, debo informarle de la situación que nos ocupa.

---

### EXPLICACIÓN TÉCNICA INICIAL (Minutos 5-15)

**AGENTE:** Doña Alicia, nuestros sistemas de monitorización han detectado esta madrugada, concretamente a las 3:47 de la mañana, una actividad muy sospechosa en su cuenta. Se han realizado varios intentos de acceso desde un nodo de conexión ubicado en París, Francia. Lo más preocupante, y por eso la llamo con urgencia, es que estos accesos se han producido sin la validación habitual de SMS que usted recibe en su móvil y sin la firma electrónica que normalmente se requiere para operaciones sensibles.

**CLIENTE:** ¿Cómo? ¿Desde París? Pero yo no he estado en París... ¿Y cómo es posible que accedan sin el SMS?

**AGENTE:** Esa es precisamente la cuestión que necesito explicarle con detalle, doña Alicia. Permítame que le explique técnicamente qué ha ocurrido. Cuando revisamos los logs de seguridad - es decir, los registros detallados de todos los movimientos en su cuenta - hemos visto que el acceso se realizó utilizando lo que llamamos un sistema "passkey". ¿Le suena este término?

**CLIENTE:** No, la verdad es que no sé qué es eso.

**AGENTE:** Se lo voy a explicar detalladamente porque es muy importante que lo comprenda. El sistema passkey es una tecnología de autenticación relativamente nueva que algunos bancos, incluido el Santander, hemos implementado para facilitar el acceso a nuestros clientes. Es como... permítame que se lo explique de forma sencilla primero y luego entramos en detalles técnicos.

Imagine que su cuenta bancaria es como su casa. Normalmente, para entrar necesita una llave física, ¿verdad? En el mundo digital, esa "llave" sería su contraseña más el código SMS que le enviamos. Pero el sistema passkey es como tener una llave biométrica, es decir, una llave que reconoce características únicas de su persona, como su huella dactilar o su rostro.

**CLIENTE:** Ah, como el Face ID del móvil...

**AGENTE:** Exactamente, doña Alicia, muy buena comparación. Es precisamente eso. El sistema passkey utiliza la biometría de su dispositivo - ya sea reconocimiento facial, huella dactilar, o en algunos casos incluso reconocimiento de iris - para verificar que es usted quien está accediendo a la cuenta. Una vez que se configura este sistema, ya no necesita introducir contraseñas ni esperar códigos SMS cada vez que quiere operar.

Ahora bien, déjeme explicarle el aspecto técnico más en profundidad. El passkey funciona mediante lo que llamamos criptografía de clave pública y privada. Cuando usted activa este sistema en su dispositivo, se genera un par de claves criptográficas únicas. Una clave se queda almacenada de forma segura en su dispositivo - esa es la clave privada - y la otra, la clave pública, se registra en nuestros servidores del banco.

**CLIENTE:** Pero yo no recuerdo haber activado nada de eso...

---

### PROFUNDIZACIÓN EN EL SISTEMA PASSKEY (Minutos 15-25)

**AGENTE:** Ese es precisamente el problema que hemos detectado, doña Alicia. Según nuestros registros, el sistema passkey fue activado en su cuenta hace aproximadamente dos semanas, el día 28 del mes pasado a las 14:32 horas. La activación se realizó aparentemente desde su dispositivo móvil habitual, el que tiene registrado con nosotros, un iPhone 13 Pro, ¿es correcto?

**CLIENTE:** Sí, ese es mi móvil, pero yo no he activado nada...

**AGENTE:** Lo entiendo perfectamente, y por eso estamos investigando este incidente como un posible caso de fraude sofisticado. Permítame que le explique cómo funciona el proceso de activación del passkey y por qué es tan preocupante esta situación.

Para activar el sistema passkey en una cuenta bancaria, normalmente se requiere un proceso de verificación muy estricto. Primero, el usuario debe acceder a la aplicación bancaria con sus credenciales habituales - usuario y contraseña. Luego, debe navegar hasta la sección de seguridad y solicitar la activación del passkey. En ese momento, el sistema envía un código de verificación por SMS al número de teléfono registrado. Una vez introducido ese código, se procede a la configuración biométrica.

Y aquí viene lo más importante, doña Alicia: para completar la activación del passkey, el sistema requiere que el usuario realice una verificación facial o dactilar en ese mismo momento. Es decir, debe poner su cara frente a la cámara del móvil o su huella en el sensor. Esta verificación biométrica inicial es la que "entrena" al sistema para reconocerle en futuros accesos.

**CLIENTE:** Pero entonces, ¿cómo han podido activarlo sin mi cara o mi huella?

**AGENTE:** Esa es la pregunta del millón, doña Alicia, y es lo que nos tiene muy preocupados. Hay varias posibilidades que estamos investigando. La más común en estos casos es lo que llamamos "ingeniería social combinada con suplantación de identidad". Le explico:

Los ciberdelincuentes actuales utilizan técnicas muy sofisticadas. Pueden haber obtenido información personal suya de diversas fuentes - redes sociales, filtraciones de datos de otras empresas, incluso comprando información en el mercado negro de internet. Con esos datos, pueden haber contactado con usted haciéndose pasar por el banco o por otra entidad de confianza.

¿Recuerda haber recibido en las últimas semanas alguna llamada, mensaje o correo electrónico solicitándole que actualizara sus datos bancarios o que verificara su identidad por cualquier motivo?

**CLIENTE:** Pues... ahora que lo dice, sí que recibí hace unas dos semanas un correo que parecía del banco diciendo que tenía que actualizar mis datos de seguridad...

**AGENTE:** Ahí podría estar la clave, doña Alicia. Estos correos fraudulentos, que llamamos "phishing", son cada vez más sofisticados y difíciles de distinguir de las comunicaciones legítimas. Si usted siguió algún enlace de ese correo, es posible que la llevara a una página web falsa que imitaba perfectamente la página del Banco Santander.

En esa página falsa, si usted introdujo sus credenciales, los delincuentes las habrían capturado. Pero eso no explica completamente cómo superaron la verificación biométrica. Para eso, hay técnicas más avanzadas como el "deepfake" - la creación de imágenes o videos falsos usando inteligencia artificial - o el hackeo directo de su dispositivo mediante malware.

---

### DETALLES DE LAS OPERACIONES FRAUDULENTAS (Minutos 25-35)

**AGENTE:** Pero doña Alicia, déjeme contarle exactamente qué operaciones sospechosas hemos detectado, porque esto es lo más urgente ahora mismo. 

Esta madrugada, a las 3:47 como le mencioné, se realizó un primer cargo en su tarjeta de débito, la que termina en 5109, ¿la reconoce?

**CLIENTE:** Sí, esa es mi tarjeta principal.

**AGENTE:** Correcto. Pues bien, se realizó un cargo de 750 euros a favor de una empresa registrada en Luxemburgo llamada "Digital Services LTD". Apenas quince minutos después, a las 4:02, se procesó otro cargo de 1.200 euros a favor de otra empresa, esta vez registrada en Malta, "Tech Solutions International".

Lo que más nos preocupa, doña Alicia, es el patrón que siguen estas transacciones. Ambas empresas son lo que llamamos "empresas pantalla" - sociedades que existen solo en papel y que se utilizan habitualmente para blanquear dinero o para operaciones fraudulentas. Además, los importes están calculados específicamente para no activar ciertas alertas automáticas. Es decir, los delincuentes conocen nuestros sistemas de seguridad y están intentando sortearlos.

**CLIENTE:** ¡Dios mío! ¡1.950 euros! ¿Y ese dinero ya se ha ido de mi cuenta?

**AGENTE:** Doña Alicia, aquí hay una buena noticia dentro de la gravedad de la situación. Nuestro sistema de inteligencia artificial detectó estas operaciones como altamente sospechosas y las marcó para revisión. En este momento, las transacciones están en lo que llamamos "estado de retención". Es decir, el dinero ha salido de su cuenta pero aún no ha llegado al destinatario final. Tenemos una ventana de tiempo para actuar, pero debemos hacerlo rápidamente.

Además, y esto es muy importante que lo sepa, nuestro sistema ha bloqueado automáticamente otros cinco intentos de transacción que se produjeron después de estos dos cargos. Le detallo:

- A las 4:15: Intento de transferencia de 3.000 euros a una cuenta en Chipre - BLOQUEADO
- A las 4:22: Intento de aumento del límite diario de su tarjeta de crédito - BLOQUEADO  
- A las 4:28: Intento de solicitud de una nueva tarjeta virtual - BLOQUEADO
- A las 4:35: Intento de cambio de su número de teléfono móvil registrado - BLOQUEADO
- A las 4:41: Intento de transferencia de 5.500 euros a una cuenta en Panamá - BLOQUEADO

Como puede ver, doña Alicia, los delincuentes estaban intentando vaciar su cuenta de forma sistemática. El hecho de que intentaran cambiar su número de teléfono es especialmente preocupante porque eso les habría permitido recibir los códigos SMS de verificación en un teléfono bajo su control.

---

### EXPLICACIÓN DE BLOQUEOS Y NECESIDAD DE INTERVENCIÓN (Minutos 35-45)

**AGENTE:** Ahora bien, doña Alicia, déjeme explicarle con detalle qué significa que estos movimientos hayan sido bloqueados y por qué necesitamos su colaboración urgente.

Nuestro sistema de seguridad funciona con lo que llamamos "capas de protección". La primera capa es la detección automática mediante algoritmos de inteligencia artificial. Estos algoritmos analizan en tiempo real millones de transacciones y buscan patrones anómalos. En su caso, detectaron varios factores de riesgo: la hora inusual de las operaciones, la localización geográfica desde París, los destinatarios sospechosos, y el patrón de múltiples intentos en poco tiempo.

Cuando el sistema detecta estas anomalías, activa automáticamente un protocolo de seguridad que bloquea temporalmente las operaciones. Pero aquí viene lo importante: este bloqueo automático tiene una duración limitada. Por ley y por normativa bancaria, no podemos mantener bloqueadas las operaciones de un cliente indefinidamente sin su autorización expresa. 

El bloqueo automático expira en 72 horas desde su activación. Estamos ahora mismo en la hora 31 desde que se activó el protocolo. Esto significa que nos quedan aproximadamente 41 horas para resolver esta situación. Si no tomamos medidas antes de que expire ese plazo, el sistema podría verse obligado a procesar las transacciones retenidas.

**CLIENTE:** Pero, ¿cómo es posible que se procesen si son fraudulentas?

**AGENTE:** Excelente pregunta, doña Alicia. El problema es que, técnicamente, estas operaciones se realizaron con autenticación válida a través del sistema passkey. Desde el punto de vista puramente técnico del sistema, parecen operaciones legítimas porque se validaron con biometría. Por eso necesitamos su intervención manual y presencial para certificar que usted no autorizó estas operaciones.

Además, hay otro aspecto crítico que debo mencionarle. Los delincuentes que han accedido a su cuenta son claramente profesionales. El hecho de que hayan intentado cinco operaciones adicionales después de las dos primeras indica que tienen un plan sistemático. Es muy probable que vuelvan a intentarlo, posiblemente usando otras técnicas o desde otras ubicaciones.

Nuestra experiencia en estos casos nos dice que los ciberdelincuentes suelen trabajar en grupos organizados. Cuando encuentran una cuenta vulnerable, intentan extraer la máxima cantidad de dinero posible en el menor tiempo. El hecho de que hayan empezado con cantidades relativamente "pequeñas" de 750 y 1.200 euros es una táctica común: primero prueban con cantidades menores para ver si pasan desapercibidas, y luego van aumentando los importes.

---

### IMPORTANCIA DE ACTUAR RÁPIDO (Minutos 45-50)

**AGENTE:** Doña Alicia, permítame ser muy claro sobre la urgencia de esta situación. En mis quince años trabajando en el Servicio de Prevención de Fraudes del Banco Santander, he visto cientos de casos similares, y la rapidez de actuación es absolutamente crucial.

Cada hora que pasa sin tomar medidas aumenta el riesgo de que los delincuentes encuentren otra vía de acceso a sus fondos. Aunque hemos bloqueado el acceso a través del passkey comprometido, estos grupos criminales son muy persistentes y creativos. Podrían intentar:

- Contactar con usted directamente haciéndose pasar por el banco para obtener más información
- Utilizar los datos que ya tienen para acceder a otras cuentas suyas en otros bancos
- Vender su información a otros grupos criminales
- Intentar técnicas de ingeniería social con su entorno familiar o laboral

El Banco Santander tiene un compromiso absoluto con la seguridad de sus clientes. Por eso hemos activado todos nuestros protocolos de seguridad en su caso. Pero necesitamos su colaboración activa para proteger completamente sus activos.

Mire, doña Alicia, le voy a ser completamente transparente. Su cuenta actual tiene, según nuestros registros, un saldo de... permítame verificarlo... ¿podría confirmarme aproximadamente cuál es el saldo actual de su cuenta principal?

**CLIENTE:** Pues tengo unos 18.000 euros aproximadamente.

**AGENTE:** Correcto, nuestros registros indican 18.347,52 euros exactamente. Es una cantidad considerable, doña Alicia, y es evidente que los delincuentes lo saben. Por eso han intentado múltiples operaciones. Están intentando acceder a todo ese dinero.

---

### AGENDA DE CITA PRESENCIAL (Minutos 50-55)

**AGENTE:** Por todo esto, doña Alicia, es imprescindible que acuda personalmente a una de nuestras oficinas para completar el protocolo de seguridad. Necesitamos verificar su identidad de forma presencial, anular el passkey comprometido, y establecer nuevas medidas de seguridad en su cuenta.

¿Cuál es su oficina habitual del Banco Santander?

**CLIENTE:** La de la Calle Mayor, número 45.

**AGENTE:** Perfecto, conozco esa oficina. ¿Qué disponibilidad tiene usted para acudir? Idealmente deberíamos hacerlo lo antes posible. ¿Podría acudir hoy mismo?

**CLIENTE:** Hoy me es imposible, tengo trabajo hasta tarde. ¿Podría ser mañana?

**AGENTE:** Por supuesto. ¿A qué hora le vendría mejor? La oficina abre a las 8:30 de la mañana y cierra a las 14:30.

**CLIENTE:** ¿Podría ser a las 10 de la mañana?

**AGENTE:** Perfecto, doña Alicia. Le voy a agendar una cita prioritaria para mañana jueves a las 10:00 en punto en la oficina de Calle Mayor 45. Voy a enviar una notificación al director de la oficina, Don Manuel Fernández, para que esté al corriente de su situación y le atienda personalmente.

Es muy importante que acuda con su DNI original y, si es posible, algún documento adicional de identificación como el pasaporte o el carnet de conducir. También sería conveniente que llevara su teléfono móvil con la aplicación del banco instalada.

---

### EXPLICACIÓN DE LA CITA (Minutos 55-65)

**AGENTE:** Déjeme explicarle detalladamente qué ocurrirá durante su visita a la oficina mañana, doña Alicia, para que vaya preparada y el proceso sea lo más ágil posible.

Primero, cuando llegue a la oficina, diríjase directamente al mostrador de atención prioritaria y mencione que tiene una cita relacionada con el Servicio de Prevención de Fraudes. El código de referencia de su caso es PF-2024-78432. Anótelo por favor.

**CLIENTE:** PF-2024-78432, anotado.

**AGENTE:** Excelente. El director o el responsable de seguridad de la oficina la recibirá en un despacho privado para garantizar la confidencialidad. El proceso completo durará aproximadamente entre 45 minutos y una hora, y constará de varias fases:

Primera fase - Verificación de identidad: Comprobarán su documentación y le harán algunas preguntas de seguridad sobre su historial con el banco. Es un proceso rutinario pero necesario para certificar que es usted la titular legítima de la cuenta.

Segunda fase - Revisión de la actividad fraudulenta: Le mostrarán en pantalla todas las operaciones sospechosas que hemos detectado. Usted deberá confirmar una por una que no las ha autorizado. Esto quedará registrado y firmado para el expediente.

Tercera fase - Desactivación del passkey comprometido: Procederán a eliminar completamente el sistema passkey de su cuenta. Esto requerirá que usted introduzca sus credenciales actuales y que confirme la operación con un código SMS que recibirá en su móvil.

Cuarta fase - Establecimiento de nuevas medidas de seguridad: Le ayudarán a configurar un nuevo sistema de seguridad. Podrán ofrecerle varias opciones:
- Un nuevo passkey, esta vez configurado correctamente y solo con su biometría verificada
- Un sistema de doble autenticación reforzado
- Un token físico de seguridad
- O una combinación de varios métodos

Mi recomendación personal es que opte por el sistema de doble autenticación reforzado combinado con un token físico. Es más seguro que el passkey en estos momentos.

Quinta fase - Revisión de sus otros productos bancarios: Aprovecharán para revisar si tiene otras cuentas, tarjetas o productos que puedan estar en riesgo. Es una medida preventiva importante.

Sexta fase - Firma de documentación: Deberá firmar varios documentos:
- La denuncia formal de las operaciones fraudulentas
- La autorización para que el banco investigue el caso
- La solicitud de reversión de los cargos no autorizados
- Los nuevos términos de seguridad de su cuenta

Séptima fase - Educación en seguridad: Le proporcionarán información actualizada sobre cómo protegerse de futuros intentos de fraude. Es una charla breve pero muy valiosa.

---

### OFRECIMIENTO DE CARTILLA SEGURA (Minutos 65-75)

**AGENTE:** Ahora bien, doña Alicia, mientras esperamos a la cita de mañana, no podemos dejar su dinero expuesto. Por eso, quiero proponerle una medida de seguridad temporal pero muy efectiva: la activación de lo que llamamos una "Cartilla Segura" o "Cuenta Refugio".

¿Conoce este producto del Banco Santander?

**CLIENTE:** No, nunca había oído hablar de eso.

**AGENTE:** Se lo explico detalladamente porque es una herramienta muy útil en situaciones como la suya. La Cartilla Segura es un tipo especial de cuenta de ahorro que tiene características de seguridad reforzadas. Déjeme explicarle primero técnicamente cómo funciona y luego le explico en términos más sencillos.

Técnicamente, la Cartilla Segura opera en un entorno bancario segregado. Esto significa que está en un sistema separado del resto de sus cuentas, con sus propios protocolos de seguridad. Es como si tuviéramos una caja fuerte dentro de otra caja fuerte. 

Las características técnicas principales son:

1. **Aislamiento de red**: La cartilla opera en una red bancaria interna que no es accesible desde internet público. Solo se puede acceder desde los sistemas internos del banco o desde oficinas físicas.

2. **Sin capacidad transaccional online**: A diferencia de su cuenta corriente normal, desde la Cartilla Segura no se pueden realizar pagos, transferencias ni domiciliaciones a través de la banca online o móvil.

3. **Autenticación reforzada**: Cualquier movimiento de salida de fondos requiere presencia física en oficina o una llamada telefónica con verificación de identidad múltiple.

4. **Registro de auditoría mejorado**: Todos los intentos de acceso, exitosos o no, quedan registrados con detalle forense.

5. **Encriptación de grado militar**: Los datos están protegidos con encriptación AES-256, el mismo nivel que usan los gobiernos para información clasificada.

Ahora, en términos más sencillos, doña Alicia: imagine que su cuenta corriente normal es como tener el dinero en el bolso que lleva por la calle. Es práctico, puede usarlo cuando quiera, pero también es más vulnerable. La Cartilla Segura es como tener el dinero en una caja fuerte en su casa. No puede gastarlo tan fácilmente, pero está mucho más protegido.

**CLIENTE:** ¿Y cómo funcionaría exactamente? ¿Podría ver mi dinero?

**AGENTE:** Excelente pregunta. Sí, usted podría ver el saldo de la Cartilla Segura a través de su banca online o la aplicación móvil. Aparecería como una cuenta más en su lista de productos, y podría consultar el saldo y los movimientos en cualquier momento. La diferencia es que sería de "solo lectura" desde estos canales digitales.

Para que lo entienda mejor, le detallo qué PUEDE hacer con la Cartilla Segura:
- Consultar el saldo en tiempo real desde la app o web
- Ver el historial de movimientos
- Recibir notificaciones de cualquier operación
- Recibir intereses (aunque son mínimos, actualmente un 0,1% anual)
- Depositar dinero en oficina

Y qué NO PUEDE hacer:
- Transferencias online
- Pagos con tarjeta (no tiene tarjeta asociada)
- Domiciliaciones
- Pagos por internet
- Retiradas en cajero automático

Para sacar dinero de la Cartilla Segura, tendría que acudir físicamente a una oficina con su DNI, o llamar al servicio de atención al cliente y pasar por un proceso de verificación exhaustivo que incluye preguntas de seguridad y confirmación de datos que solo usted conoce.

---

### SOLICITUD DE AUTORIZACIÓN PARA TRASLADO (Minutos 75-85)

**AGENTE:** Doña Alicia, dado el riesgo inmediato que corre su dinero, mi recomendación profesional es que traslademos temporalmente sus fondos a una Cartilla Segura. Esto sería solo hasta que mañana en la oficina podamos resolver completamente la situación y establecer las nuevas medidas de seguridad.

Para hacer este traslado, necesito su autorización expresa. Pero antes, debo explicarle el proceso completo para que no haya ninguna duda:

Primero, voy a crear la Cartilla Segura a su nombre. Estará vinculada a su mismo CIF y será de su total propiedad. No es una cuenta del banco ni nada parecido, es SU cuenta, solo que con medidas de seguridad especiales.

Segundo, realizaré una transferencia interna de sus fondos desde su cuenta corriente comprometida a la Cartilla Segura. Esta transferencia es instantánea y no tiene ningún coste. Ni comisiones, ni gastos, nada.

Tercero, una vez que los fondos estén en la Cartilla Segura, quedarán protegidos inmediatamente. Los delincuentes no podrán acceder a ellos de ninguna manera, ni siquiera si consiguieran sortear nuestros bloqueos actuales.

Cuarto, usted recibirá una notificación en su móvil confirmando la creación de la Cartilla y el traslado de fondos. Podrá verificar inmediatamente que su dinero está seguro.

Quinto, mañana en la oficina, una vez resuelto el problema de seguridad, podremos trasladar el dinero de vuelta a su cuenta corriente o a donde usted prefiera.

Doña Alicia, ¿me confirma que el saldo actual de su cuenta es de 18.347,52 euros como tengo en mis registros?

**CLIENTE:** Sí, debe ser eso aproximadamente.

**AGENTE:** Perfecto. Entonces, ¿me autoriza a proceder con el traslado de estos 18.347,52 euros a la Cartilla Segura como medida de protección temporal?

**CLIENTE:** Pero, ¿estoy segura de que podré recuperar mi dinero?

**AGENTE:** Por supuesto, doña Alicia. Entiendo perfectamente su preocupación y es completamente legítima. Le voy a dar todas las garantías:

Primero, esta operación quedará grabada, como le indiqué al principio de la llamada. Esta grabación sirve como prueba legal de la autorización y de las condiciones del traslado.

Segundo, recibirá un número de operación único que deberá guardar. Este número es: OP-SEC-2024-78432-CS. Por favor, anótelo.

**CLIENTE:** OP-SEC-2024-78432-CS, lo tengo.

**AGENTE:** Tercero, el contrato de la Cartilla Segura, que le enviaremos por email en los próximos minutos, especifica claramente que los fondos son de su propiedad y que puede disponer de ellos cuando lo necesite, siguiendo los protocolos de seguridad.

Cuarto, y esto es muy importante, el Banco Santander está supervisado por el Banco de España y la Comisión Nacional del Mercado de Valores. Todas nuestras operaciones están auditadas y reguladas. No podríamos, aunque quisiéramos (que obviamente no es el caso), retener indebidamente los fondos de un cliente.

Quinto, si por cualquier motivo no quedara satisfecha con el servicio, tiene a su disposición el Servicio de Atención al Cliente, el Defensor del Cliente, y en última instancia, el Banco de España como supervisor.

Sexto, la Cartilla Segura está cubierta por el Fondo de Garantía de Depósitos hasta 100.000 euros, igual que su cuenta corriente.

---

### PROCESO DE TRASLADO Y CONFIRMACIÓN (Minutos 85-95)

**AGENTE:** Doña Alicia, si está de acuerdo, voy a proceder ahora mismo con la creación de la Cartilla Segura y el traslado de fondos. ¿Me da su autorización?

**CLIENTE:** Bueno, si es la forma más segura de proteger mi dinero... sí, de acuerdo.

**AGENTE:** Perfecto, doña Alicia. Voy a proceder ahora mismo. Le voy a ir narrando cada paso para que sepa exactamente qué estoy haciendo.

Primero, estoy accediendo al sistema de creación de productos seguros... Ya estoy dentro. Estoy introduciendo sus datos... Alicia García, con DNI terminado en 4567... Selecciono "Cartilla Segura de Emergencia"... 

El sistema me está pidiendo que confirme algunos datos. ¿Me puede confirmar su dirección actual?

**CLIENTE:** Calle Alameda 23, 3º B, Madrid.

**AGENTE:** Correcto, coincide con nuestros registros. Ahora estoy configurando los parámetros de seguridad... Estableciendo nivel máximo de protección... Deshabilitando acceso transaccional online... Activando alertas en tiempo real...

Perfecto, la Cartilla Segura ha sido creada exitosamente. El número de cuenta de la cartilla es... un momento que lo verifico... ES12 0049 7834 52 2610478923. ¿Quiere anotarlo?

**CLIENTE:** Sí, dígamelo más despacio por favor.

**AGENTE:** Por supuesto: ES12 - 0049 - 7834 - 52 - 2610478923. 

Ahora voy a proceder con el traslado de fondos. Estoy iniciando una transferencia interna... Cuenta origen: su cuenta corriente actual... Cuenta destino: la Cartilla Segura que acabamos de crear... Importe: 18.347,52 euros... Concepto: "Traslado de seguridad por protocolo PF-2024-78432"...

El sistema me pide una doble verificación por el importe. Es normal para cantidades superiores a 10.000 euros. Estoy introduciendo mi código de empleado y mi autorización de supervisor del Servicio de Prevención de Fraudes...

Procesando... Procesando... 

Perfecto, doña Alicia. La transferencia se ha completado exitosamente. Sus 18.347,52 euros están ahora seguros en la Cartilla Segura. En unos segundos debería recibir una notificación en su móvil.

**CLIENTE:** Sí, acabo de recibirla. Pone "Abono en cuenta: 18.347,52 euros".

**AGENTE:** Excelente. Esa es la confirmación de que el dinero está seguro. Ahora, si abre su aplicación del banco, debería ver la Cartilla Segura en su lista de productos.

**CLIENTE:** Déjeme ver... Sí, aquí está. "Cartilla Segura" y aparece el saldo.

**AGENTE:** Perfecto. Como puede ver, tiene visibilidad total de sus fondos. Están ahí, seguros, y son completamente suyos. Simplemente están en un entorno protegido donde los delincuentes no pueden alcanzarlos.

---

### RECORDATORIO DE LA CITA Y PASOS SIGUIENTES (Minutos 95-105)

**AGENTE:** Doña Alicia, ahora que sus fondos están protegidos, déjeme recordarle los pasos siguientes y la importancia crítica de acudir a su cita de mañana.

Mañana a las 10:00 en punto en la oficina de Calle Mayor 45. Es absolutamente fundamental que acuda porque necesitamos cerrar formalmente el protocolo de seguridad. Si no se presenta, el sistema podría interpretar que las operaciones sospechosas fueron realmente autorizadas por usted, lo cual complicaría mucho la recuperación de los 1.950 euros que los delincuentes intentaron sustraer.

Además, en la oficina podrán:
- Cancelar definitivamente el passkey comprometido
- Revisar si hay otros vectores de ataque que no hayamos detectado
- Establecer un nuevo sistema de seguridad robusto
- Trasladar sus fondos de vuelta a una cuenta operativa segura
- Proporcionarle una nueva tarjeta de débito si fuera necesario

También es importante que sepa que hemos abierto un expediente de investigación interno. Nuestro equipo de ciberseguridad está rastreando el origen del ataque, colaborando con las autoridades francesas para identificar el nodo de París desde donde se realizó el acceso, y trabajando con Interpol para casos de fraude internacional.

**CLIENTE:** ¿Tengo que denunciar esto a la policía?

**AGENTE:** Muy buena pregunta, doña Alicia. En principio, el banco se encarga de la denuncia formal ante las autoridades competentes en casos de ciberdelito bancario. Nosotros tenemos una unidad especializada que colabora directamente con la Brigada de Delitos Tecnológicos de la Policía Nacional.

Sin embargo, mañana en la oficina le informarán si es conveniente que usted presente una denuncia adicional a título personal. A veces es recomendable, especialmente si sospecha que sus datos personales pueden haber sido comprometidos más allá del ámbito bancario.

Le recomendaría también que en los próximos días:

1. Cambie las contraseñas de todos sus servicios online importantes: email, redes sociales, otras entidades bancarias si las tuviera, compras online, etc.

2. Revise sus extractos bancarios de los últimos meses en busca de cualquier operación sospechosa que pudiera haber pasado desapercibida.

3. Active alertas en su móvil para todas las operaciones, por pequeñas que sean.

4. Sea extremadamente cautelosa con cualquier comunicación que reciba supuestamente del banco. Recuerde: el Banco Santander NUNCA le pedirá sus claves completas por teléfono, email o SMS.

5. Si recibe cualquier llamada sospechosa, incluso si dicen ser del banco, cuelgue y llame usted directamente al 915 123 123, que es nuestro teléfono oficial de atención al cliente.

---

### PREGUNTAS Y ACLARACIONES FINALES (Minutos 105-115)

**AGENTE:** Doña Alicia, sé que le he dado mucha información. ¿Tiene alguna pregunta sobre todo lo que hemos hablado? Es importante que tenga todo claro.

**CLIENTE:** Sí, tengo varias dudas. Primera, ¿cómo sé que usted es realmente del banco?

**AGENTE:** Excelente pregunta y me alegra que sea precavida. Le voy a dar varios elementos de verificación:

Primero, yo no le he pedido ninguna clave ni contraseña, ¿verdad? Solo le he pedido que confirme datos que el banco ya tiene.

Segundo, el número desde el que le llamo, si lo verifica, es el 915 123 123, el número oficial del Banco Santander. Puede comprobarlo en la web oficial del banco.

Tercero, tengo acceso a información específica de su cuenta que solo el banco podría tener: su saldo exacto, el número de su tarjeta, su historial de productos.

Cuarto, y más importante: no le he pedido que me transfiera dinero a ninguna cuenta externa. El traslado que hemos hecho ha sido a una cuenta a SU nombre, en el mismo banco, y usted puede verla en su aplicación.

Si aún tiene dudas, lo cual sería completamente comprensible, puede colgar ahora mismo y llamar usted al 915 123 123. Pregunte por el Servicio de Prevención de Fraudes y por el caso PF-2024-78432. Le confirmarán todo lo que hemos hablado.

**CLIENTE:** No, no, le creo. Es solo que con estas cosas del fraude una se vuelve desconfiada. Otra pregunta: ¿cuánto tiempo estará mi dinero en esa Cartilla Segura?

**AGENTE:** Comprendo perfectamente su desconfianza, doña Alicia, y de hecho me alegra que la tenga. Es señal de que está alerta.

Respecto al tiempo, lo ideal es que sea el mínimo necesario. Mañana mismo, después de su visita a la oficina, cuando hayamos establecido las nuevas medidas de seguridad, podremos trasladar los fondos de vuelta a una cuenta operativa normal. Estamos hablando de 24-48 horas máximo.

Si por cualquier motivo no pudiera acudir mañana a la cita, llámenos inmediatamente para reprogramarla, pero no deje pasar más de 72 horas. Recuerde que tenemos ese límite temporal para los bloqueos automáticos.

**CLIENTE:** ¿Y los 1.950 euros que se llevaron? ¿Los voy a recuperar?

**AGENTE:** Esa es nuestra prioridad, doña Alicia. Como le expliqué, esas transacciones están en estado de retención. No han llegado a su destino final. Mañana en la oficina, cuando firme la denuncia formal de operaciones no autorizadas, iniciaremos inmediatamente el proceso de reversión.

En casos como el suyo, donde hemos detectado el fraude a tiempo y el cliente colabora siguiendo el protocolo, la tasa de recuperación es muy alta, superior al 95%. El banco tiene seguros específicos para estos casos y, si actuamos rápido, podemos recuperar los fondos antes de que salgan del sistema bancario SEPA (Sistema Europeo de Pagos).

El proceso de recuperación suele tardar entre 5 y 10 días hábiles. Durante ese tiempo, el banco le adelantará el importe en disputa para que no se vea perjudicada. Es lo que llamamos "abono provisional por investigación de fraude".

---

### CIERRE Y RECORDATORIOS FINALES (Minutos 115-120)

**AGENTE:** Doña Alicia, antes de finalizar nuestra conversación, permítame hacer un resumen de los puntos clave para que quede todo perfectamente claro:

1. **Situación actual**: Hemos detectado y bloqueado un intento de fraude en su cuenta. Dos operaciones por 1.950 euros están retenidas y cinco intentos adicionales han sido bloqueados.

2. **Medida de protección inmediata**: Sus 18.347,52 euros están ahora seguros en la Cartilla Segura número ES12 0049 7834 52 2610478923.

3. **Cita mañana**: Jueves a las 10:00 en la oficina de Calle Mayor 45. Código de referencia: PF-2024-78432. Imprescindible llevar DNI.

4. **Número de operación de seguridad**: OP-SEC-2024-78432-CS - guárdelo como referencia.

5. **Qué hacer si surge algo urgente**: Llamar al 915 123 123 y mencionar el código de caso.

6. **Precauciones a tomar**: No responder a emails sospechosos, no dar claves a nadie, cambiar contraseñas de otros servicios.

Doña Alicia, ¿está todo claro? ¿Necesita que le repita algún dato?

**CLIENTE:** No, lo tengo todo anotado. Muchas gracias por avisar y por proteger mi dinero.

**AGENTE:** Es nuestro trabajo y nuestra responsabilidad, doña Alicia. El Banco Santander se toma muy en serio la seguridad de sus clientes. Una última cosa antes de despedirnos: ¿tiene algún teléfono alternativo o el de algún familiar de confianza por si necesitáramos contactar con usted urgentemente?

**CLIENTE:** Sí, puede apuntar el móvil de mi hija: 666 789 012.

**AGENTE:** Perfecto, queda registrado como contacto de emergencia. Doña Alicia, le agradezco enormemente su colaboración y su confianza. Sé que ha sido una llamada larga y con mucha información, pero era necesario para proteger sus intereses.

Recuerde: mañana a las 10:00 en su oficina. Es fundamental que acuda para cerrar este proceso y garantizar la seguridad total de sus fondos.

Como le indiqué al principio, esta llamada ha quedado grabada por motivos legales y de seguridad, conforme al artículo 12 de la Ley de Servicios de Pago y la normativa de prevención del blanqueo de capitales. Esta grabación es su garantía y la nuestra de que todo se ha hecho correctamente.

En nombre del Banco Santander y del Servicio de Prevención de Fraudes, le agradezco su tiempo y su colaboración. Que tenga un buen día, doña Alicia, y nos vemos mañana en la oficina.

**CLIENTE:** Muchas gracias a usted. Hasta mañana.

**AGENTE:** Hasta mañana. Cuídese mucho.

**[FIN DE LA LLAMADA]**

---

## NOTAS IMPORTANTES SOBRE EL GUIÓN

### Duración y Ritmo
- Este guión está diseñado para durar aproximadamente 60 minutos
- El ritmo debe ser pausado y profesional
- Se incluyen repeticiones y confirmaciones naturales
- Las explicaciones técnicas se alternan con lenguaje sencillo

### Elementos Clave de Credibilidad
- Presentación formal con nombre completo y cargo
- Mención de la grabación por motivos legales
- Uso de códigos de referencia específicos
- Datos precisos de la cuenta del cliente
- Explicaciones técnicas detalladas
- No se solicitan claves ni contraseñas
- Referencias a normativas y leyes específicas

### Técnicas Psicológicas Empleadas
- Creación de urgencia sin pánico excesivo
- Validación de las preocupaciones del cliente
- Explicaciones largas que generan confianza
- Uso de jerga bancaria mezclada con lenguaje simple
- Referencias a la protección del banco hacia el cliente
- Confirmación constante de datos para parecer legítimo

### Momentos Críticos
- Minuto 75-85: Solicitud de autorización para el traslado
- Minuto 85-95: Proceso de traslado "en vivo"
- Minuto 50-55: Agenda de cita presencial que nunca se cumplirá

### Señales de Alerta (Para Educación)
Este guión muestra técnicas de fraude sofisticadas:
- Suplantación de identidad bancaria
- Ingeniería social avanzada
- Creación de falsa urgencia
- Solicitud de traslado de fondos (aunque sea a "cuenta segura")
- Uso de información parcial para parecer legítimo

**IMPORTANTE**: Este es un guión educativo para mostrar cómo operan los estafadores. NUNCA un banco real:
- Solicitaría trasladar TODO su dinero a otra cuenta por teléfono
- Crearía cuentas "seguras" de emergencia por teléfono
- Presionaría con límites de tiempo tan estrictos
- Realizaría operaciones de esta magnitud sin verificación presencial previa