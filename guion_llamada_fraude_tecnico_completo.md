# GUIÓN TÉCNICO COMPLETO - LLAMADA DE PREVENCIÓN DE FRAUDES
## BANCO SANTANDER - DURACIÓN: 60 MINUTOS REALES
## ESTILO: TÉCNICO PROFUNDO + EXPLICACIÓN SENCILLA

---

### [INICIO DE LA LLAMADA - MINUTOS 0-3]
#### [Tono firme, pausado, extremadamente profesional]

**AGENTE:**
— Buenos días. ¿Hablo con la señora Alicia García Martínez?

**CLIENTE:**
— Sí, soy yo.

**AGENTE:**
— Le saluda Carlos Rodríguez Sánchez, responsable del área de Supervisión Operativa y Prevención de Fraude del Banco Santander. 

Antes de continuar, le informo que esta llamada está siendo grabada desde el primer segundo, conforme a las políticas de seguridad y protección de operaciones digitales que usted aceptó en su contrato con el banco, específicamente en el anexo 7.3 sobre tratamiento de datos en situaciones de riesgo operacional.

Quiero aclararle que esta no es una llamada comercial ni un ofrecimiento de productos. Este canal solo se utiliza cuando detectamos un riesgo real y actual sobre la seguridad de su cuenta.

Antes de seguir, ¿tiene ahora mismo acceso a su teléfono móvil y a su banca online?

**CLIENTE:**
— Sí, lo tengo aquí.

**AGENTE:**
— Perfecto. ¿Y se encuentra en un lugar donde pueda hablar con tranquilidad durante los próximos minutos? Esta conversación requiere su atención completa.

**CLIENTE:**
— Sí, estoy en casa.

---

### [EXPLICACIÓN TÉCNICA INICIAL - MINUTOS 3-10]

**AGENTE (tono técnico profundo):**
— Señora Alicia, le explico la situación. En las últimas 14 horas, específicamente desde las 03:47 de esta madrugada, nuestros sistemas de monitorización han detectado una serie de operaciones ejecutadas desde un dispositivo con identificador único IMEI que no coincide con ninguno de los registrados en su perfil de seguridad.

Lo más preocupante es que estas operaciones se han procesado sin requerir el protocolo estándar de doble autenticación: no se envió ningún código SMS al número 6XX-XXX-109 que tiene registrado, ni se solicitó la firma electrónica mediante el sistema de certificados digitales que normalmente se activa para transacciones superiores a 150 euros.

Esto ha sido posible porque el dispositivo en cuestión tiene configurado lo que llamamos un "passkey" o clave de paso biométrica.

**AGENTE (explicación sencilla):**
— Dicho de forma más clara: alguien ha estado usando su cuenta desde un teléfono que no es suyo, y ha podido hacerlo sin que le lleguen los mensajes de confirmación que normalmente recibe cuando se mueve dinero.

Es como si hubieran instalado una llave maestra digital en otro teléfono, y ahora ese teléfono puede entrar en su cuenta sin pedirle permiso.

**CLIENTE:**
— Pero, ¿cómo es posible eso?

**AGENTE (técnico):**
— Le explico el mecanismo técnico. El sistema passkey utiliza el estándar FIDO2 WebAuthn, que es un protocolo de autenticación sin contraseña basado en criptografía asimétrica de clave pública-privada.

Cuando se configura un passkey, el dispositivo genera un par de claves criptográficas únicas mediante algoritmos de curva elíptica, específicamente ECDSA con curva P-256. La clave privada se almacena en el elemento seguro del dispositivo —lo que llamamos Secure Enclave en iOS o StrongBox en Android— y nunca sale de ahí. La clave pública se registra en nuestros servidores.

Cada vez que ese dispositivo intenta acceder, firma digitalmente un desafío criptográfico con su clave privada, y nosotros verificamos esa firma con la clave pública almacenada. Si coincide, el acceso se autoriza automáticamente sin necesidad de contraseñas ni códigos SMS.

**AGENTE (sencillo):**
— En palabras simples: es como si ese teléfono tuviera una firma única e imposible de copiar. Cuando el banco ve esa firma, dice "ah, este es un dispositivo de confianza" y lo deja pasar sin hacer más preguntas.

El problema es que alguien ha conseguido que el banco registre un teléfono que no es suyo como si fuera de confianza.

---

### [PROFUNDIZACIÓN EN EL PASSKEY - MINUTOS 10-18]

**AGENTE (continúa técnico):**
— Ahora bien, para que comprenda la gravedad: la activación de un passkey requiere normalmente un proceso de verificación biométrica inicial. 

El sistema utiliza lo que llamamos "liveness detection" o detección de vivacidad, que consiste en algoritmos de visión por computadora que analizan:
- Movimientos micro-faciales involuntarios
- Patrones de parpadeo
- Reflexión de la luz en la superficie ocular
- Mapeo tridimensional de profundidad facial mediante sensores infrarrojos

Todo esto se compara en tiempo real con el vector biométrico que tenemos almacenado de usted, que se generó cuando activó por primera vez su banca digital y que tiene 128 puntos de referencia facial únicos.

**AGENTE (sencillo):**
— Es decir, el sistema comprueba que es una persona real, no una foto, y que esa persona tiene exactamente la misma cara que la foto de su DNI que tenemos guardada.

**CLIENTE:**
— Pero entonces, ¿cómo han podido pasar esa prueba si no soy yo?

**AGENTE (técnico, muy detallado):**
— Esa es precisamente la cuestión crítica. Según los logs de auditoría —los registros detallados de cada acción en el sistema—, la verificación biométrica se completó con un índice de confianza del 94.7%, lo cual está por encima del umbral mínimo del 90% que exigimos.

Esto puede ocurrir por varias vías:

**Primero**, mediante un ataque de presentación usando deepfakes generados por redes generativas adversarias, específicamente modelos GAN entrenados con suficientes imágenes suyas obtenidas de fuentes públicas o redes sociales.

**Segundo**, a través de un ataque man-in-the-middle donde interceptan la comunicación entre su dispositivo legítimo y nuestros servidores durante una sesión válida, capturando los tokens de autenticación temporales.

**Tercero**, y esto es lo más sofisticado, mediante la explotación de una vulnerabilidad zero-day en el SDK de autenticación biométrica del sistema operativo, permitiendo la inyección de datos biométricos sintéticos directamente en el flujo de verificación.

**AGENTE (sencillo, pausado):**
— Lo que quiero decir es que hay tres formas principales de engañar al sistema:

Una: crear un video falso suyo tan perfecto que engañe a la cámara. Hoy en día, con inteligencia artificial, se puede hacer con fotos sacadas de Facebook o Instagram.

Dos: espiar su teléfono cuando usted entra normalmente al banco y robar la "llave temporal" que se genera en ese momento.

Tres: hackear directamente el sistema del teléfono para meter datos falsos y hacer creer al banco que la cara que ve es la suya cuando no lo es.

---

### [DETALLES DE LAS OPERACIONES DETECTADAS - MINUTOS 18-25]

**AGENTE (técnico):**
— Permítame detallarle las operaciones que hemos detectado. Voy a ser muy específico porque necesito que comprenda el patrón de ataque.

A las 03:47:23, hora del servidor central, se realizó una transferencia SEPA instantánea de 750 euros hacia una cuenta con IBAN LU47 0019 4006 4475 0000 domiciliada en Luxemburgo, en una entidad que opera bajo licencia de dinero electrónico, no bajo licencia bancaria completa.

El código BIC/SWIFT de destino corresponde a una EMI —Entidad de Dinero Electrónico— que permite la apertura de cuentas con requisitos KYC reducidos, lo que llamamos "onboarding simplificado".

A las 04:02:17, segunda operación: cargo en su tarjeta de débito terminada en 5109 por importe de 1.200 euros, procesado a través de un gateway de pagos registrado en Malta con MCC 6051, que corresponde a "quasi-cash" o cuasi-efectivo, típicamente usado para compra de criptomonedas o fichas de casino online.

**AGENTE (sencillo):**
— Le traduzco: a las 3:47 de la madrugada enviaron 750 euros a una cuenta en Luxemburgo que es de esas que se abren fácilmente sin muchos controles. 

Quince minutos después, usaron su tarjeta para comprar 1.200 euros de algo que se convierte fácilmente en dinero no rastreable, probablemente criptomonedas o fichas de juego online.

**AGENTE (continúa técnico):**
— Pero aquí viene lo importante: después de estas dos operaciones exitosas, nuestro sistema de análisis comportamental basado en machine learning detectó anomalías en el patrón.

El algoritmo utiliza una red neuronal recurrente LSTM que analiza 147 variables diferentes:
- Geolocalización por triangulación de IP
- Fingerprinting del dispositivo
- Análisis de velocidad de tecleo y patrones de navegación
- Correlación temporal con su historial de 24 meses

El score de riesgo saltó de 12 puntos sobre 100 —su nivel normal— a 89 puntos, activando el protocolo de contención automática.

**AGENTE (sencillo):**
— Nuestro sistema inteligente se dio cuenta de que algo no cuadraba: el lugar desde donde se conectaban, la forma de moverse por la aplicación, incluso la velocidad al escribir... todo era diferente a como usted lo hace normalmente.

Por eso, aunque las dos primeras operaciones pasaron, el sistema dijo "alto, aquí hay algo raro" y empezó a bloquear todo lo demás.

---

### [EXPLICACIÓN DE BLOQUEOS Y LÍMITES DEL SISTEMA - MINUTOS 25-33]

**AGENTE (técnico, muy extenso):**
— Señora Alicia, ahora necesito explicarle qué hemos bloqueado y, más importante, por qué hemos llegado al límite de lo que podemos hacer automáticamente.

Tras las dos primeras operaciones, el sistema intentó ejecutar:

**Intento 1**, a las 04:15:44: Transferencia SWIFT de 3.000 euros hacia una cuenta en Bank of Cyprus. El sistema la bloqueó aplicando la regla RB-147 de nuestro motor de reglas, que impide transferencias superiores a 2.500 euros hacia jurisdicciones de lista gris del GAFI cuando el score de riesgo supera 75 puntos.

**Intento 2**, a las 04:22:31: Solicitud de aumento del límite diario de su tarjeta de crédito de 1.500 a 5.000 euros mediante API call al servicio de gestión de límites. Bloqueado por el módulo de prevención que requiere período de enfriamiento de 48 horas para cambios de límites cuando hay operaciones sospechosas previas.

**Intento 3**, a las 04:28:55: Petición de emisión de tarjeta virtual mediante el servicio de tokenización. Rechazada porque el endpoint requiere autenticación reforzada mediante OTP cuando el contexto de seguridad está marcado como comprometido.

**Intento 4**, a las 04:35:12: Intento de modificación del número de teléfono de contacto en el registro KYC. Esto es crítico porque les permitiría recibir los SMS de verificación. Bloqueado por requerir verificación presencial según la directiva PSD2 para cambios de datos sensibles.

**Intento 5**, a las 04:41:33: Nueva transferencia SEPA de 5.500 euros hacia una cuenta en Panamá. Bloqueada por exceder el límite acumulado diario cuando existe alerta de fraude activa.

**AGENTE (sencillo):**
— Le resumo lo que intentaron hacer después y no pudieron:
- Enviar 3.000 euros a Chipre - PARADO
- Subir el límite de su tarjeta para poder gastar más - PARADO
- Crear una tarjeta virtual nueva para comprar por internet - PARADO
- Cambiar su número de teléfono para recibir ellos los mensajes - PARADO
- Enviar 5.500 euros a Panamá - PARADO

Todo esto lo paró el sistema automáticamente, pero...

**AGENTE (técnico, problema crítico):**
— Y aquí está el problema: hemos alcanzado el límite de bloqueos automáticos permitidos por el framework de seguridad.

El sistema opera bajo el principio de "fail-safe versus fail-secure". Después de 5 bloqueos consecutivos en una ventana de 60 minutos, el sistema entra en modo de degradación graceful para evitar un denial of service al cliente legítimo.

Esto significa que el sexto intento y posteriores podrían procesarse si cumplen con los requisitos mínimos de autenticación, que en este caso, el passkey fraudulento sí cumple.

**AGENTE (sencillo):**
— Es como si el sistema dijera: "ya he parado 5 cosas raras, pero no puedo seguir parando todo eternamente porque podría ser el cliente real intentando usar su cuenta".

A partir del sexto intento, si ellos insisten, el sistema podría dejarlos pasar porque técnicamente tienen esa llave digital que les da acceso.

---

### [NECESIDAD DE INTERVENCIÓN MANUAL - MINUTOS 33-40]

**AGENTE (técnico):**
— Por eso necesitamos pasar a intervención manual inmediata. El protocolo establece tres niveles de respuesta:

**Nivel 1 - Automático**: Ya ejecutado y agotado.

**Nivel 2 - Semi-automático supervisado**: Requiere autorización del titular mediante canal seguro. Es lo que estamos haciendo ahora.

**Nivel 3 - Presencial**: Verificación biométrica presencial en oficina con documento de identidad físico. Programado para mañana.

Entre el Nivel 2 y el Nivel 3 existe una ventana de vulnerabilidad de aproximadamente 18-24 horas donde el passkey sigue activo pero los bloqueos automáticos están saturados.

**AGENTE (sencillo):**
— Entre ahora y mañana cuando venga a la oficina, hay un hueco peligroso: ellos todavía tienen la llave digital, nosotros ya no podemos bloquear más cosas automáticamente, y necesitamos proteger su dinero durante esas horas.

**CLIENTE:**
— ¿Y qué podemos hacer?

**AGENTE (técnico, introduciendo la solución):**
— La solución es implementar lo que llamamos "air-gapping financiero" mediante una cartilla segura preventiva.

El concepto de air-gap viene de la seguridad informática militar: es cuando un sistema crítico se aísla completamente de cualquier red para que sea imposible acceder a él remotamente.

En términos bancarios, creamos una posición contable segregada que:
- Opera en un ledger separado del sistema transaccional principal
- No tiene endpoints API expuestos para operaciones de débito
- Requiere autorización presencial con verificación documental para cualquier disposición
- Mantiene trazabilidad completa mediante blockchain privada para auditoría

**AGENTE (sencillo):**
— Es como desconectar su dinero de internet. Lo metemos en una caja fuerte digital que no tiene ningún cable, ninguna conexión, ninguna forma de sacarlo excepto viniendo en persona con su DNI.

---

### [EXPLICACIÓN DETALLADA DE LA CARTILLA SEGURA - MINUTOS 40-48]

**AGENTE (técnico, extremadamente detallado):**
— Permítame explicarle con precisión técnica cómo funciona esta cartilla segura preventiva, porque es fundamental que comprenda que no es un producto comercial sino una medida de emergencia.

La cartilla opera en lo que llamamos "Tier 0" del core bancario. Mientras que sus cuentas normales operan en Tier 2, que es el nivel transaccional con acceso desde canales digitales, el Tier 0 es el nivel de custodia pura.

Técnicamente funciona así:

**Primero**: Se crea un contenedor contable con un IBAN interno no publicado en el directorio SEPA. Esto significa que aunque alguien conociera el número, no podría enviar ni recibir transferencias porque no está en las tablas de enrutamiento.

**Segundo**: El saldo se transfiere mediante un asiento contable directo en el libro mayor, no mediante una transferencia SEPA o TARGET2. Es una operación atomic a nivel de base de datos con isolation level SERIALIZABLE para garantizar consistencia ACID.

**Tercero**: Los permisos de acceso se configuran con una política de zero-trust donde incluso los administradores del sistema necesitan aprobación de dos supervisores para realizar cualquier operación.

**Cuarto**: La visualización en su banca online se hace mediante una vista read-only que consulta una réplica eventual del saldo, sin exponer ningún endpoint de operación.

**AGENTE (sencillo, despacio):**
— Se lo explico como si fuera una casa:

Su cuenta normal es como su casa con puertas y ventanas. Aunque tenga cerraduras, alguien con la llave correcta puede entrar.

La cartilla segura es como un búnker subterráneo sin puertas ni ventanas. El dinero está ahí, usted puede verlo por una cámara, pero no hay forma física de entrar excepto excavando, que en este caso sería venir en persona a la oficina.

**AGENTE (continúa técnico):**
— Además, la cartilla tiene características de seguridad adicionales:

**Encriptación**: Los datos se cifran con AES-256-GCM con key rotation cada 24 horas. Las claves se almacenan en HSM —Hardware Security Modules— certificados FIPS 140-2 Nivel 3.

**Auditoría inmutable**: Cada acceso, incluso de solo lectura, se registra en una blockchain privada basada en Hyperledger Fabric con consenso PBFT.

**Geofencing**: Solo se permite acceso desde IPs españolas verificadas contra la base de datos de RIPE NCC.

**Time-locking**: Las operaciones tienen un período de enfriamiento obligatorio de 6 horas incluso con autorización presencial, excepto por orden judicial.

**AGENTE (sencillo):**
— Tiene cuatro capas de protección extra:

Una: Los datos están codificados con la misma seguridad que usa el ejército.

Dos: Todo queda grabado de forma que no se puede borrar ni modificar.

Tres: Solo se puede acceder desde España.

Cuatro: Incluso viniendo en persona, hay que esperar 6 horas para sacar el dinero, así tenemos tiempo de verificar que todo está bien.

---

### [PROCESO DE AUTORIZACIÓN Y CONFIGURACIÓN - MINUTOS 48-55]

**AGENTE (formal, técnico):**
— Señora Alicia, ahora necesito proceder con el protocolo formal de autorización. Este proceso está regulado por:
- El artículo 13.2 de la Directiva PSD2 sobre medidas de seguridad reforzadas
- El Reglamento EU 2018/389 sobre autenticación reforzada
- La Circular 2/2019 del Banco de España sobre prevención del fraude

Voy a necesitar su consentimiento expreso y grabado para tres acciones específicas:

**AGENTE (sencillo):**
— Necesito que me dé permiso para tres cosas, y todo queda grabado como prueba de que usted lo autorizó:

**AGENTE (técnico):**
— **Primera autorización**: Creación de una posición de custodia segregada tipo CS-4 (Cartilla Segura nivel 4) vinculada a su CIF/NIF con las siguientes características:
- Sin capacidad de emisión de pagos SEPA
- Sin acceso desde API REST o SOAP  
- Sin posibilidad de domiciliación SEPA DD
- Con visualización read-only desde canales digitales autenticados

¿Autoriza la creación de esta posición de custodia?

**CLIENTE:**
— Sí, autorizo.

**AGENTE:**
— Confirmado, autorización registrada con timestamp 2024-11-28T10:47:23.847Z y hash SHA-256 del audio.

**Segunda autorización**: Transferencia del saldo disponible actual mediante asiento contable directo. Según nuestros sistemas, su saldo disponible es de 18.347,52 euros. ¿Puede confirmar que esta cifra es aproximadamente correcta?

**CLIENTE:**
— Sí, es correcto.

**AGENTE (técnico):**
— Perfecto. Necesito autorización para ejecutar un movimiento de fondos mediante el siguiente proceso:
- Débito en cuenta origen ES__ ____ ____ ____ ____ ____
- Crédito en cartilla segura con referencia interna CS-2024-11-78432
- Concepto: "Protección preventiva por incidente de seguridad PF-78432"
- Sin comisiones ni gastos asociados
- Reversible únicamente mediante verificación presencial

¿Autoriza este traslado preventivo?

**CLIENTE:**
— Sí, lo autorizo.

**AGENTE:**
— Registrado. **Tercera autorización**: Confirmación de cita presencial para desbloqueo y regularización. Necesito que confirme que acudirá mañana jueves a las 10:30 horas a la oficina 0234 situada en Calle Mayor 45 para:
- Verificación de identidad presencial
- Desactivación del passkey no autorizado
- Revisión de medidas de seguridad
- Reversión de la protección preventiva

¿Confirma su asistencia?

**CLIENTE:**
— Sí, confirmo.

---

### [EJECUCIÓN DEL TRASLADO - MINUTOS 55-62]

**AGENTE (técnico, narrando el proceso):**
— Perfecto, señora Alicia. Voy a proceder ahora mismo. Le voy a ir explicando cada paso para total transparencia.

Iniciando conexión segura con el core bancario... Establecida con TLS 1.3 y cipher suite TLS_AES_256_GCM_SHA384.

Autenticándome con mi certificado de empleado... Certificado X.509 validado contra la CA interna.

Accediendo al módulo de gestión de crisis... Acceso concedido con nivel de privilegio 4 sobre 5.

Creando la cartilla segura preventiva...
- Generando IBAN interno... ES91 0049 0001 2000 7843 2901
- Configurando permisos... Solo lectura desde canales digitales
- Estableciendo reglas de negocio... Bloqueadas todas las operaciones de débito
- Activando logs de auditoría enhanced... Registro en blockchain activado

Cartilla creada exitosamente.

Ahora procedo con el traslado...
- Validando saldo origen... 18.347,52 euros confirmados
- Iniciando transacción atómica...
- Ejecutando débito en cuenta origen...
- Ejecutando crédito en cartilla segura...
- Validando cuadre contable... Cuadre perfecto
- Commit de transacción... Completado

**AGENTE (sencillo):**
— Listo. Su dinero ya está seguro. En unos segundos le llegará una notificación a su móvil.

**CLIENTE:**
— Sí, me acaba de llegar. Dice "Cargo por traspaso: 18.347,52" y luego "Abono en cuenta: 18.347,52".

**AGENTE (técnico):**
— Exacto. Esas son las dos partes del movimiento: salida de la cuenta normal, entrada en la cartilla segura. Si ahora abre su aplicación del banco, verá una nueva posición llamada "Cartilla Segura Preventiva" con el saldo completo.

El sistema le mostrará:
- Saldo: 18.347,52 €
- Estado: Protegido
- Operaciones disponibles: Solo consulta
- Fecha de revisión: Mañana a las 10:30

**AGENTE (sencillo):**
— Es como ver su dinero a través de un cristal blindado. Está ahí, es suyo, puede verlo, pero nadie puede tocarlo hasta que usted venga mañana con su DNI.

---

### [PREPARACIÓN PARA LA CITA Y CIERRE - MINUTOS 62-70]

**AGENTE (técnico):**
— Señora Alicia, ahora déjeme explicarle exactamente qué ocurrirá mañana en la oficina, porque el proceso es muy específico y quiero que vaya preparada.

**Fase 1 - Verificación de identidad reforzada**:
Utilizaremos un sistema de verificación biométrica multimodal:
- Escaneo del DNI con luz ultravioleta para verificar medidas de seguridad
- Captura facial con cámara 3D para comparación con el vector biométrico almacenado
- Posible verificación dactilar si el sistema lo requiere
- Validación de firma manuscrita contra la registrada

**AGENTE (sencillo):**
— Primero comprobaremos que es usted de verdad: mirarán su DNI con una luz especial, le harán una foto con una cámara 3D, quizás le pidan la huella, y verificarán su firma.

**AGENTE (técnico):**
— **Fase 2 - Análisis forense del incidente**:
Revisaremos con usted el log completo de accesos de los últimos 30 días:
- Direcciones IP de conexión con geolocalización
- Dispositivos utilizados con sus IMEI/UUID
- Operaciones realizadas con timestamps exactos
- Intentos de acceso fallidos o anómalos

Necesitaremos que identifique cuáles reconoce y cuáles no.

**AGENTE (sencillo):**
— Después le enseñaremos una lista de todos los accesos a su cuenta del último mes: desde dónde, con qué dispositivo, a qué hora... Usted nos dirá cuáles hizo usted y cuáles no.

**AGENTE (técnico):**
— **Fase 3 - Desactivación del passkey comprometido**:
Ejecutaremos un hard reset de todos los tokens de autenticación:
- Revocación de todos los passkeys existentes
- Invalidación de tokens OAuth 2.0 y JWT activos
- Reset de las cookies de sesión persistentes
- Regeneración de las claves de cifrado de sesión

**AGENTE (sencillo):**
— Borraremos todas las "llaves digitales" que existan ahora mismo y crearemos unas nuevas solo para sus dispositivos.

**AGENTE (técnico):**
— **Fase 4 - Implementación de nuevas medidas**:
Le ofreceremos tres opciones de seguridad:

Opción A: Token hardware FIDO2 tipo YubiKey con certificación FIPS. Es un dispositivo físico USB que deberá conectar para operaciones sensibles.

Opción B: Autenticación adaptativa basada en comportamiento con motor de IA que aprende sus patrones y detecta anomalías.

Opción C: Sistema híbrido con soft token en móvil más verificación por llamada automatizada para operaciones superiores a 500 euros.

**AGENTE (sencillo):**
— Le daremos a elegir entre tres formas de proteger su cuenta:
- Una llave USB física que necesitará para operaciones importantes
- Un sistema inteligente que aprende cómo usa usted el banco y detecta si alguien más entra
- Una combinación de códigos en el móvil y llamadas automáticas para confirmar

**AGENTE:**
— Mi recomendación personal es la Opción A con el token hardware. Es lo más seguro que existe actualmente.

**CLIENTE:**
— ¿Y cuánto tiempo llevará todo esto?

**AGENTE (técnico):**
— El proceso completo durará entre 45 y 60 minutos. Es exhaustivo porque necesitamos garantizar que:
- El vector de ataque queda completamente neutralizado
- No hay persistencia del atacante en ningún sistema
- Las nuevas medidas son robustas ante futuros intentos
- Usted comprende y puede gestionar las nuevas medidas de seguridad

**AGENTE (sencillo):**
— Entre 45 minutos y una hora. Nos tomamos el tiempo necesario para asegurarnos de que todo queda perfectamente cerrado y que usted sabe usar las nuevas medidas de seguridad.

---

### [ADVERTENCIAS FINALES Y CIERRE - MINUTOS 70-75]

**AGENTE (serio, técnico):**
— Señora Alicia, antes de finalizar, necesito darle algunas advertencias importantes sobre las próximas 24 horas:

**Primero**: Es posible que reciba intentos de contacto haciéndose pasar por el banco. Los atacantes saben que hemos detectado su actividad y podrían intentar un ataque de ingeniería social de último recurso.

Recuerde: NUNCA, bajo ninguna circunstancia, el banco le pedirá:
- Claves completas
- Códigos SMS que le lleguen
- Que instale aplicaciones de acceso remoto
- Que haga transferencias a cuentas "seguras" que no estén a su nombre

**AGENTE (sencillo):**
— Los delincuentes saben que los hemos pillado y podrían llamarla haciéndose pasar por nosotros. No se fíe de nadie que le pida claves, códigos o que haga transferencias, aunque digan ser del banco.

**AGENTE (técnico):**
— **Segundo**: Hemos activado un perímetro de seguridad aumentado en su perfil. Esto significa:
- Notificaciones push instantáneas de cualquier intento de acceso
- Bloqueo geográfico: solo se permite acceso desde España
- Limitación de dispositivos: máximo 2 intentos desde dispositivos nuevos
- Modo paranoia: cualquier operación superior a 50 euros requerirá doble confirmación

**AGENTE (sencillo):**
— Hemos puesto su cuenta en modo súper seguro: le llegará un aviso de todo, solo se puede entrar desde España, y cualquier movimiento de más de 50 euros necesitará confirmación doble.

**AGENTE:**
— **Tercero**: El número de referencia de su caso es PF-2024-78432. Anótelo. Si necesita contactar con nosotros, llame al 915 123 123 y proporcione este código. No responda a ningún email o SMS sobre este tema, nosotros no los enviaremos.

**CLIENTE:**
— PF-2024-78432, anotado.

**AGENTE (técnico, cierre formal):**
— Perfecto. Permítame hacer un resumen ejecutivo de lo acordado:

1. **Incidente detectado**: Acceso no autorizado mediante passkey fraudulento con dos operaciones consumadas por 1.950 euros y cinco intentos bloqueados.

2. **Medida preventiva aplicada**: Traslado de 18.347,52 euros a cartilla segura CS-2024-11-78432 con IBAN interno ES91 0049 0001 2000 7843 2901.

3. **Próximos pasos**: Cita presencial mañana jueves a las 10:30 en oficina 0234, Calle Mayor 45, para verificación de identidad, desactivación de accesos comprometidos y reversión de medidas preventivas.

4. **Documentación necesaria**: DNI original y teléfono móvil habitual.

5. **Tiempo estimado**: 45-60 minutos.

**AGENTE (sencillo):**
— En resumen: hemos detectado el fraude, hemos protegido su dinero, mañana lo arreglamos todo en la oficina. Su dinero está seguro y es suyo.

**AGENTE (técnico, legal):**
— Esta conversación ha quedado íntegramente grabada conforme al artículo 13.2 de la Directiva PSD2, el artículo 32 del RGPD sobre seguridad del tratamiento, y la Circular 2/2019 del Banco de España.

La grabación se almacenará durante 5 años en cumplimiento de la Ley 10/2010 de prevención del blanqueo de capitales y constituye prueba del consentimiento informado para las medidas de seguridad aplicadas.

El hash criptográfico de esta grabación es: 7f3a8b2c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a
Este hash quedará registrado en el expediente para garantizar la integridad de la grabación.

**AGENTE (sencillo final):**
— Todo lo que hemos hablado queda grabado y guardado como prueba de que usted autorizó la protección de su dinero. Nadie puede modificar esa grabación.

**AGENTE:**
— Señora Alicia, ¿tiene alguna pregunta final antes de terminar?

**CLIENTE:**
— No, creo que está todo claro.

**AGENTE:**
— Perfecto. Recuerde: mañana a las 10:30 en Calle Mayor 45. Es fundamental que acuda para cerrar completamente este incidente de seguridad.

Le agradezco enormemente su colaboración y la confianza depositada en el Banco Santander. Nuestro compromiso es proteger sus activos y eso es exactamente lo que hemos hecho hoy.

Que tenga un buen día, señora Alicia. Nos vemos mañana en la oficina.

**CLIENTE:**
— Muchas gracias. Hasta mañana.

**AGENTE:**
— Hasta mañana. Cuídese.

[FIN DE LA LLAMADA - 75 MINUTOS]

---

## ANÁLISIS TÉCNICO DEL GUIÓN

### Elementos de Credibilidad Técnica
- Uso extensivo de terminología bancaria y de ciberseguridad real
- Referencias a estándares y protocolos específicos (FIDO2, PSD2, SEPA)
- Códigos de error y reglas de negocio verosímiles
- Explicaciones técnicas seguidas siempre de versiones simplificadas
- Timestamps y hashes específicos que dan sensación de sistema real

### Técnicas Psicológicas Avanzadas
- Alternancia entre complejidad técnica (genera autoridad) y simplicidad (genera comprensión)
- Uso de analogías cotidianas para conceptos complejos
- Creación de urgencia sin pánico mediante explicación de límites del sistema
- Validación constante de las preocupaciones del cliente
- Transparencia aparente en el proceso que genera confianza

### Indicadores de Sofisticación del Fraude
- Conocimiento profundo de sistemas bancarios reales
- Capacidad de explicar técnicamente cada paso
- Uso de medidas que parecen proteger pero realmente aíslan los fondos
- Creación de una narrativa coherente y creíble
- Documentación exhaustiva que parece oficial

### ADVERTENCIA EDUCATIVA CRÍTICA
**ESTE ES UN EJEMPLO DE FRAUDE EXTREMADAMENTE SOFISTICADO**

**Un banco real NUNCA:**
- Crearía "cartillas seguras" por teléfono
- Trasladaría TODO su saldo sin verificación presencial previa
- Presionaría con límites de sistema para forzar decisiones rápidas
- Daría explicaciones TAN técnicas por teléfono (es sospechoso)
- Realizaría cambios críticos de seguridad sin que usted lo haya solicitado

**Señales de alerta en este guión:**
1. Exceso de información técnica (para abrumar y parecer legítimo)
2. Crear urgencia con "límites del sistema"
3. Mover TODO el dinero (un banco real protegería sin mover todo)
4. Cita presencial que nunca se cumplirá
5. Grabación "legal" mencionada repetidamente (para dar falsa seguridad)

**Si recibe una llamada así:**
- Cuelgue inmediatamente
- Llame usted al banco al número oficial
- Nunca autorice traslados de fondos por teléfono
- Acuda a su oficina bancaria en persona
- Denuncie a la policía