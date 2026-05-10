/**
 * CertiCore — Motor de Expediente Forense
 * Captura silenciosa de leads hacia n8n con fail-safe obligatorio.
 * Privacidad por Diseño: sin logs, sin alerts, sin bloquear al usuario.
 */
(function () {
  'use strict';

  // ── Configuración ────────────────────────────────────────────
  var WEBHOOK_URL =
    'https://tu-n8n.com/webhook-test/lead-certilab'; // ← URL de prueba (cambiar en producción)

  var REDIRECT_URL_BASE = '/resultado-auditoria/';
  var DELAY_MS = 2500; // Tiempo mínimo de animación "Conectando con Sede Electrónica…"

  // ── Utilidades ────────────────────────────────────────────────
  function $ (sel, ctx) { return (ctx || document).querySelector(sel); }

  /** Desinfecta y estructura la dirección antes del envío */
  function limpiarDireccion (raw) {
    var texto = (raw || '').trim()
      .replace(/\s{2,}/g, ' ')           // colapsar espacios múltiples
      .replace(/[<>"']/g, '');           // eliminar caracteres peligrosos
    return texto.substring(0, 300);      // límite razonable
  }

  /** Intenta separar calle/número de población (mejor esfuerzo) */
  function parsearDireccion (texto) {
    var partes = texto.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (partes.length >= 2) {
      return { calle: partes[0], poblacion: partes.slice(1).join(', ') };
    }
    // Fallback: buscar último token largo como posible población
    var tokens = texto.split(' ');
    if (tokens.length >= 3) {
      var ultimo = tokens[tokens.length - 1];
      if (ultimo.length > 4) {
        return {
          calle: tokens.slice(0, -1).join(' '),
          poblacion: ultimo
        };
      }
      if (tokens.length >= 4) {
        var penultimo = tokens[tokens.length - 2] + ' ' + tokens[tokens.length - 1];
        return {
          calle: tokens.slice(0, -2).join(' '),
          poblacion: penultimo
        };
      }
    }
    return { calle: texto, poblacion: '' };
  }

  /** Construye URL de redirect con query params para pasar datos al resultado */
  function buildRedirectUrl (direccionLimpia, parsed, ts) {
    return REDIRECT_URL_BASE +
      '?direccion=' + encodeURIComponent(direccionLimpia) +
      '&calle=' + encodeURIComponent(parsed.calle) +
      '&poblacion=' + encodeURIComponent(parsed.poblacion) +
      '&ts=' + encodeURIComponent(ts);
  }

  // ── UI: Animación de conexión ─────────────────────────────────
  function mostrarConectando (btn, form) {
    // Guardar estado original del botón
    var htmlOriginal = btn.innerHTML;
    btn._originalHTML = htmlOriginal;

    btn.innerHTML =
      '<span class="certi-spinner"></span> Conectando con Sede Electrónica…';
    btn.disabled = true;
    btn.setAttribute('aria-busy', 'true');
    btn.classList.add('certi-connecting');

    // Deshabilitar input también
    var input = form && form.querySelector('input');
    if (input) { input.disabled = true; }
  }

  // ── Core: Envío al webhook ────────────────────────────────────
  /**
   * iniciarExpediente(rawDireccion)
   * 1. Limpia y estructura los datos
   * 2. Envía asíncronamente a n8n (sin esperar respuesta)
   * 3. Redirige SIEMPRE a resultado-auditoria.html con datos por query string
   *
   * @param {string} rawDireccion — texto crudo del input del usuario
   * @param {HTMLElement} btn — botón que disparó la acción (opcional)
   * @param {HTMLFormElement} form — formulario contenedor (opcional)
   */
  function iniciarExpediente (rawDireccion, btn, form) {
    var direccionLimpia = limpiarDireccion(rawDireccion);
    if (!direccionLimpia) {
      // Sin datos: redirigir igualmente (la página mostrará placeholders)
      window.location.href = REDIRECT_URL_BASE;
      return;
    }

    // Animación visual mientras se procesa
    if (btn) { mostrarConectando(btn, form); }

    var parsed = parsearDireccion(direccionLimpia);
    var ts = new Date().toISOString();

    var payload = {
      direccion_o_referencia: direccionLimpia,
      calle: parsed.calle,
      poblacion: parsed.poblacion,
      timestamp: ts,
      origen: 'Buscador_Home',
      estado_expediente: 'iniciado'
    };

    // ── Envío asíncrono con fallback silencioso ──────────────────
    var redirectUrl = buildRedirectUrl(direccionLimpia, parsed, ts);

    var redirigir = function () {
      window.location.href = redirectUrl;
    };

    // Programar redirección garantizada tras DELAY_MS (pase lo que pase)
    var timerRedirect = setTimeout(redirigir, DELAY_MS);

    try {
      fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        // No esperamos respuesta: modo fire-and-forget con timeout corto
        signal: (function () {
          var ctrl = new AbortController();
          setTimeout(function () { ctrl.abort(); }, 4000);
          return ctrl.signal;
        })()
      })
        .then(function () {
          // Éxito silencioso — nada que mostrar al usuario
        })
        .catch(function () {
          // Fallo silencioso — el timerRedirect ya garantiza la redirección
        });
    } catch (_) {
      // Si fetch() lanza sincrónicamente (raro), el timer ya está corriendo
    }
  }

  // ── Binding automático al DOM ─────────────────────────────────
  function bind () {
    var form = $('#certi-expediente-form');
    if (!form) { return; }

    var input = form.querySelector('input');
    var btn = form.querySelector('button, [type="submit"], .certi-submit');

    if (!input || !btn) { return; }

    // Submit por botón
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      iniciarExpediente(input.value, btn, form);
    });

    // Submit por tecla Enter en el input
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        iniciarExpediente(input.value, btn, form);
      }
    });
  }

  // ── Inicialización ────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }

  // Exponer para uso programático externo
  window.CertiCore = { iniciarExpediente: iniciarExpediente };
})();