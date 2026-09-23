# Feature Specification: Login y Control de Acceso

**Feature Branch**: `002-login-control-acceso`

**Created**: 2026-09-23

**Status**: Draft

**Input**: User description: "/specify login Desarrollar el módulo de autenticación (Login) y gestión de control de acceso para la aplicación web de gestión comercial, integrándose con la base de datos SQLite existente (archivo app.db, tabla \"usuarios\"). Requisitos: validar credenciales mediante correo y hash seguro, restringir la creación de usuarios a Administrador, mostrar errores claros sin revelar detalles internos, confirmar acceso exitoso y redirigir a la vista comercial principal, cumplir seguridad por defecto, validación server-side, diseño responsive/moderno e incluir pruebas automatizadas básicas."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Iniciar sesión con credenciales válidas (Priority: P1)

Como usuario registrado de la aplicación comercial, quiero iniciar sesión con mi correo y
contraseña para acceder de forma segura a la vista comercial principal.

**Why this priority**: El acceso autenticado es la puerta de entrada a las operaciones y datos
comerciales protegidos.

**Independent Test**: Con un usuario existente en `app.db`, introducir sus credenciales válidas
y comprobar que recibe confirmación, una sesión autenticada y acceso a la vista comercial
principal.

**Acceptance Scenarios**:

1. **Given** un usuario activo con correo registrado y contraseña válida, **When** envía el
   formulario de login, **Then** el sistema valida el hash almacenado, confirma el acceso y lo
   redirige a la vista comercial principal.
2. **Given** un usuario autenticado, **When** accede a una vista protegida, **Then** el sistema
   reconoce su sesión y permite la operación autorizada según su rol.

---

### User Story 2 - Rechazar credenciales inválidas de forma segura (Priority: P1)

Como usuario que intenta acceder, necesito recibir una indicación clara cuando el acceso no es
válido sin que la aplicación exponga información que facilite ataques.

**Why this priority**: Los errores de autenticación deben ser comprensibles para la persona,
pero no deben permitir distinguir innecesariamente si existe un correo o revelar detalles
internos.

**Independent Test**: Probar un correo inexistente, una contraseña incorrecta y entradas
inválidas; verificar que el acceso no se crea, se muestra un mensaje seguro y la aplicación
permanece disponible.

**Acceptance Scenarios**:

1. **Given** un correo no registrado o una contraseña incorrecta, **When** se intenta iniciar
   sesión, **Then** el sistema rechaza el acceso con un mensaje genérico que indique que las
   credenciales no son válidas y no revele cuál dato falló.
2. **Given** campos vacíos, malformados o excesivamente largos, **When** se envía el formulario,
   **Then** el servidor rechaza la entrada, muestra una indicación comprensible y no consulta ni
   modifica datos de forma insegura.
3. **Given** un intento fallido, **When** se revisan los mensajes y registros visibles al
   usuario, **Then** no aparecen hashes, contraseñas, consultas, rutas internas ni trazas.

---

### User Story 3 - Controlar la creación de usuarios por rol (Priority: P1)

Como responsable de seguridad, necesito que solo las personas con rol Administrador puedan
registrar nuevos usuarios para evitar altas no autorizadas.

**Why this priority**: La creación de identidades modifica el perímetro de acceso de toda la
aplicación y debe estar restringida por mínimo privilegio.

**Independent Test**: Probar la operación de creación con una sesión Administrador, una sesión
Ventas, una sesión Gerencia y una sesión no autenticada; comprobar que solo Administrador puede
completarla.

**Acceptance Scenarios**:

1. **Given** una sesión autenticada con rol Administrador, **When** solicita crear un usuario
   válido, **Then** el sistema autoriza la operación y persiste el nuevo usuario mediante el
   flujo definido para credenciales seguras.
2. **Given** una sesión autenticada con rol Ventas o Gerencia, **When** solicita acceder a la
   creación de usuarios, **Then** el sistema deniega la operación con un mensaje claro de falta
   de permisos y no crea ni modifica registros.
3. **Given** una persona no autenticada, **When** solicita crear un usuario, **Then** el sistema
   exige autenticación y no permite acceder a la operación.

---

### User Story 4 - Usar una interfaz de acceso clara y responsive (Priority: P2)

Como usuario de la aplicación, quiero completar el login desde móvil o escritorio con una
interfaz clara, moderna y fácil de entender.

**Why this priority**: La seguridad debe coexistir con una experiencia de acceso usable y
consistente.

**Independent Test**: Completar el flujo en un viewport móvil y uno de escritorio verificando
que los campos, mensajes, foco y acciones principales son visibles y operables.

**Acceptance Scenarios**:

1. **Given** la pantalla de login en móvil o escritorio, **When** el usuario navega y completa
   los campos, **Then** la interfaz no solapa contenidos, conserva etiquetas y permite enviar o
   corregir el formulario.
2. **Given** un error de validación o autenticación, **When** se muestra el mensaje, **Then** el
   mensaje queda asociado al formulario y es comprensible sin depender únicamente del color.

### Edge Cases

- El correo debe normalizarse de forma consistente antes de buscarlo, sin aceptar espacios o
  formatos inválidos como credenciales válidas.
- La comparación de contraseñas debe ejecutarse contra el hash almacenado; nunca se debe comparar
  ni persistir la contraseña en texto plano.
- Un usuario sin rol válido, desactivado o con datos incompletos no obtiene una sesión autorizada.
- Un usuario autenticado que intenta abrir directamente una operación restringida debe recibir
  denegación de permisos y no solo una ocultación visual del enlace.
- Una sesión ausente, expirada o manipulada no debe permitir acceder a vistas protegidas.
- Un intento repetido de login fallido no debe revelar si el correo existe ni detalles de la
  implementación, y debe dejar el sistema en un estado consistente.
- La pérdida de conexión con `app.db` debe producir un mensaje seguro de indisponibilidad sin
  mostrar rutas, consultas o trazas internas.
- El doble envío del formulario no debe crear sesiones inconsistentes ni duplicar una creación
  de usuario autorizada.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST mostrar una pantalla de login con campos para correo electrónico y
  contraseña, etiquetas claras, mensajes de validación y una acción explícita de acceso.
- **FR-002**: El sistema MUST consultar el archivo SQLite `app.db` y la tabla `usuarios` para
  localizar el usuario por correo normalizado.
- **FR-003**: El sistema MUST validar la contraseña recibida contra el hash seguro almacenado en
  el registro del usuario y MUST rechazar cualquier contraseña almacenada o comparada en texto
  plano.
- **FR-004**: El sistema MUST crear una sesión autenticada solo cuando el usuario existe, sus
  credenciales son válidas y su cuenta puede acceder al sistema.
- **FR-005**: Tras un acceso válido, el sistema MUST mostrar una confirmación segura y redirigir
  al usuario a la vista comercial principal.
- **FR-006**: Ante correo inexistente o contraseña incorrecta, el sistema MUST impedir la sesión
  y mostrar un mensaje genérico y claro que no permita distinguir cuál credencial falló.
- **FR-007**: El servidor MUST validar presencia, formato, longitud y contenido permitido de las
  entradas antes de consultar o modificar la base de datos.
- **FR-008**: El sistema MUST restringir la creación de usuarios al rol `Administrador`, con la
  autorización aplicada en el backend para cada solicitud y no únicamente en la interfaz.
- **FR-009**: El sistema MUST denegar la creación de usuarios a personas no autenticadas y a
  usuarios con roles `Ventas` o `Gerencia`, sin crear cambios parciales.
- **FR-010**: El sistema MUST mostrar un mensaje claro de falta de permisos cuando un usuario
  autenticado no autorizado intente crear usuarios, sin exponer información interna.
- **FR-011**: El sistema MUST impedir el acceso a vistas comerciales protegidas cuando no exista
  una sesión válida o cuando la sesión no cumpla el permiso requerido.
- **FR-012**: El sistema MUST proteger las consultas y operaciones sobre SQLite mediante entradas
  parametrizadas o mecanismos equivalentes, sin interpolar datos recibidos del usuario.
- **FR-013**: El sistema MUST gestionar errores de base de datos y autenticación sin revelar
  hashes, contraseñas, consultas, rutas locales, trazas o detalles de infraestructura.
- **FR-014**: El sistema MUST proporcionar una interfaz responsive, moderna e intuitiva que sea
  usable en móvil y escritorio, con etiquetas asociadas, foco visible y mensajes comprensibles.
- **FR-015**: El sistema MUST incluir pruebas automatizadas básicas para acceso exitoso,
  credenciales inválidas y control de creación de usuarios por rol Administrador, Ventas,
  Gerencia y persona no autenticada.
- **FR-016**: Las pruebas MUST verificar que los intentos denegados no crean sesiones, usuarios ni
  modificaciones persistentes.

### Key Entities *(include if feature involves data)*

- **Usuario autenticable**: Registro de `usuarios` en `app.db` identificado por correo, hash de
  contraseña, rol y estado necesario para decidir si puede iniciar sesión.
- **Sesion autenticada**: Estado temporal que representa que una persona validó sus credenciales y
  puede acceder a operaciones según su rol.
- **Permiso de creación de usuarios**: Regla de autorización que permite la operación únicamente
  al rol `Administrador`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los casos de prueba con credenciales válidas crea una sesión y llega a
  la vista comercial principal.
- **SC-002**: El 100% de los casos con correo inexistente, contraseña incorrecta o entrada
  inválida rechaza el acceso sin crear sesión.
- **SC-003**: El 100% de las solicitudes de creación realizadas por Administrador se autoriza
  cuando los datos son válidos, y el 100% de las solicitudes de Ventas, Gerencia o personas no
  autenticadas se rechaza sin modificar usuarios.
- **SC-004**: Ningún mensaje visible al usuario ni registro operativo de los escenarios de prueba
  contiene contraseñas, hashes, consultas, rutas locales o trazas internas.
- **SC-005**: El 100% de las pruebas de validación rechaza entradas vacías, malformadas o fuera de
  los límites definidos antes de ejecutar operaciones de persistencia.
- **SC-006**: El flujo principal de login puede completarse en móvil y escritorio sin
  solapamientos, desplazamiento horizontal innecesario ni pérdida de mensajes o controles.
- **SC-007**: Las pruebas automatizadas del módulo son reproducibles y cubren como mínimo un
  caso exitoso, credenciales inválidas y cada resultado de autorización por rol definido.

## Assumptions

- La tabla `usuarios` ya existe en `app.db` conforme al modelo de la feature
  `001-modelo-usuarios-roles`, incluyendo correo normalizado, hash seguro y rol.
- La primera versión utiliza una sesión web gestionada por la aplicación; el mecanismo concreto
  de cookies, expiración, renovación y protección CSRF se definirá durante la planificación sin
  debilitar los requisitos de seguridad.
- Los roles reconocidos inicialmente son exactamente `Administrador`, `Ventas` y `Gerencia`.
- La vista comercial principal ya existe o se definirá como dependencia de implementación; esta
  feature solo establece la redirección posterior al login exitoso.
- La recuperación de contraseña, cierre de sesión avanzado, bloqueo progresivo, MFA y auditoría
  detallada quedan fuera de esta feature, salvo que la planificación determine que son
  imprescindibles para no introducir un riesgo de seguridad.
- La aplicación debe usar mensajes de error comprensibles, pero deliberadamente equivalentes para
  correo inexistente y contraseña incorrecta.
- Las pruebas utilizarán una base de datos aislada o datos controlados para no alterar usuarios
  reales de `app.db`.
