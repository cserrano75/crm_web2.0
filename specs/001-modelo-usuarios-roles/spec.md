# Feature Specification: Modelo Inicial de Usuarios y Roles

**Feature Branch**: `001-modelo-usuarios-roles`

**Created**: 2026-09-23

**Status**: Draft

**Input**: User description: "/specify database Crear el modelo de datos relacional inicial para la gestión de usuarios y roles. Debe incluir la tabla de usuarios con campos para identificador único, correo electrónico (único), contraseña (almacenada como hash seguro), rol (ej. Administrador, Ventas, Gerencia) y marcas de tiempo de creación/actualización. Asegurar el uso de restricciones SQL para integridad de datos."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar usuarios con identidad única (Priority: P1)

Como responsable de administración, necesito registrar usuarios con una identidad única y
sus datos mínimos de acceso para que cada persona pueda ser identificada de forma inequívoca.

**Why this priority**: La identidad del usuario es la base para controlar el acceso a toda la
aplicación comercial.

**Independent Test**: Crear un usuario válido, consultar sus datos persistidos y comprobar que
el identificador, el correo, el rol y las marcas de tiempo cumplen las reglas definidas.

**Acceptance Scenarios**:

1. **Given** que no existe un usuario con el correo indicado, **When** se registra un usuario
   con identificador, correo, hash de contraseña y rol válidos, **Then** el registro se guarda
   con un identificador único y marcas de creación y actualización.
2. **Given** que ya existe un usuario con un correo, **When** se intenta registrar otro con el
   mismo correo, **Then** la operación se rechaza por la restricción de unicidad y no se crea
   un segundo registro.

---

### User Story 2 - Asignar un rol válido (Priority: P1)

Como responsable de administración, necesito asignar a cada usuario un rol comercial válido
para que las futuras funcionalidades puedan aplicar permisos de forma consistente.

**Why this priority**: Un rol inválido o ambiguo puede conceder permisos incorrectos y afectar
la seguridad de la información.

**Independent Test**: Registrar usuarios con cada rol permitido y probar que un valor fuera del
catálogo de roles es rechazado sin persistir datos inválidos.

**Acceptance Scenarios**:

1. **Given** que el catálogo permite los roles Administrador, Ventas y Gerencia, **When** se
   registra un usuario con uno de esos roles, **Then** el registro se acepta.
2. **Given** que un valor de rol no pertenece al catálogo permitido, **When** se intenta guardar
   el usuario, **Then** la restricción de integridad rechaza la operación.

---

### User Story 3 - Mantener credenciales y trazabilidad de forma segura (Priority: P1)

Como responsable de seguridad, necesito que las credenciales no se almacenen en texto plano y
que cada usuario conserve sus marcas de creación y actualización para facilitar el control y la
trazabilidad.

**Why this priority**: La exposición de contraseñas comprometería todas las cuentas y la falta
de marcas de tiempo dificultaría auditar cambios.

**Independent Test**: Persistir un usuario, inspeccionar los campos almacenados y actualizar un
atributo permitido; comprobar que la contraseña no es legible y que la marca de actualización
cambia sin perder la de creación.

**Acceptance Scenarios**:

1. **Given** una contraseña proporcionada al crear un usuario, **When** se persiste el registro,
   **Then** solo se almacena un hash seguro y nunca la contraseña original.
2. **Given** un usuario existente, **When** se modifica su correo o rol, **Then** la marca de
   actualización refleja el cambio y la marca de creación permanece inalterada.
3. **Given** un usuario sin identificador, correo, hash de contraseña, rol o marca de creación
   obligatorios, **When** se intenta persistir el registro, **Then** la operación se rechaza por
   restricciones de obligatoriedad.

### Edge Cases

- El correo se considera único sin permitir duplicados por diferencias de mayúsculas o espacios
  que representen la misma dirección normalizada.
- Un correo vacío, con formato inválido o que exceda el límite definido se rechaza antes de
  persistir el registro.
- Un hash vacío, truncado o con formato no compatible con el mecanismo de verificación se
  rechaza; nunca se acepta una contraseña en texto plano como sustituto.
- Un identificador duplicado o con formato inválido se rechaza sin modificar el usuario ya
  existente.
- Una actualización no autorizada no debe cambiar ningún campo ni las marcas de tiempo.
- La eliminación de un usuario debe conservar la integridad referencial de futuras entidades
  que lo puedan referenciar; la política concreta de eliminación queda fuera de esta versión.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST persistir una entidad de usuario con un identificador único y no
  nulo.
- **FR-002**: El sistema MUST persistir un correo electrónico obligatorio, normalizado y único
  dentro del conjunto de usuarios.
- **FR-003**: El sistema MUST persistir únicamente un hash seguro de la contraseña; no debe
  almacenar, devolver ni registrar la contraseña en texto plano.
- **FR-004**: El sistema MUST asociar cada usuario con exactamente un rol principal obligatorio.
- **FR-005**: El sistema MUST reconocer inicialmente los roles Administrador, Ventas y Gerencia,
  y MUST rechazar cualquier otro valor no aprobado.
- **FR-006**: El sistema MUST registrar la fecha y hora de creación de cada usuario y MUST
  conservarla sin cambios durante actualizaciones posteriores.
- **FR-007**: El sistema MUST registrar la fecha y hora de actualización de cada usuario y MUST
  actualizarla cuando cambie cualquier dato persistido del usuario.
- **FR-008**: El modelo MUST aplicar restricciones de integridad de datos en la persistencia,
  incluyendo obligatoriedad, unicidad, valores válidos y formato compatible con los tipos
  definidos.
- **FR-009**: Las restricciones de integridad MUST ejecutarse en la base de datos y no depender
  únicamente de validaciones de la interfaz o de una capa de aplicación.
- **FR-010**: El sistema MUST rechazar una operación que viole una restricción sin dejar cambios
  parciales ni duplicados.
- **FR-011**: El modelo MUST permitir que futuras funcionalidades relacionen operaciones con un
  usuario sin duplicar su identidad ni su información de rol.
- **FR-012**: El acceso de administración y cualquier operación de alta o modificación MUST
  quedar sujeto a autorización por rol en el backend cuando se exponga mediante la aplicación.

### Key Entities *(include if feature involves data)*

- **Usuario**: Persona con acceso a la aplicación comercial. Incluye identificador único, correo
  normalizado, hash seguro de contraseña, rol principal y marcas de creación y actualización.
- **Rol**: Categoría de permisos asignable a un usuario. La primera versión reconoce
  Administrador, Ventas y Gerencia como valores válidos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los usuarios persistidos tiene identificador, correo, hash de
  contraseña, rol y marca de creación válidos.
- **SC-002**: El 100% de los intentos de registrar correos duplicados es rechazado sin crear un
  segundo usuario.
- **SC-003**: El 100% de los intentos de guardar roles fuera del catálogo aprobado es rechazado
  por una regla de integridad.
- **SC-004**: En una revisión de datos de prueba, el 100% de los registros contiene hashes no
  reversibles o verificables mediante el mecanismo aprobado, y ningún registro contiene la
  contraseña original.
- **SC-005**: El 100% de las actualizaciones válidas cambia la marca de actualización y conserva
  sin cambios la marca de creación.
- **SC-006**: Todas las restricciones de integridad cuentan con pruebas automatizadas que cubren
  casos válidos, duplicados, valores nulos y valores fuera de catálogo antes de pasar a la fase
  de implementación.

## Assumptions

- La primera versión asigna un único rol principal a cada usuario; la asignación de múltiples
  roles y permisos granulares queda fuera de alcance.
- Los nombres iniciales de rol son Administrador, Ventas y Gerencia; agregar o renombrar roles
  requiere una especificación posterior y una migración controlada.
- El correo se normaliza antes de evaluar unicidad, conservando una representación consistente
  para consultas y comunicación.
- El mecanismo de hash seguro será elegido durante la planificación con una alternativa vigente,
  resistente a fuerza bruta y con parámetros documentados; esta especificación no define una
  librería concreta.
- La autenticación, recuperación de contraseña, gestión de sesiones, interfaz administrativa y
  auditoría detallada quedan fuera de esta feature, excepto por las reglas de almacenamiento y
  autorización necesarias para no comprometer el modelo.
- La política de retención y eliminación de usuarios se definirá cuando existan entidades que
  referencien al usuario.
