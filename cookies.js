/**
 * Certilab — Gestión de consentimiento de cookies (RGPD)
 * v2.0 — Mayo 2026
 *
 * Comportamiento:
 *  - Muestra banner en primera visita (sin elección previa)
 *  - Guarda elección en localStorage por 365 días
 *  - Si "Aceptar todas" → se carga Meta Pixel (fbq)
 *  - Si "Solo técnicas" → no se carga Meta Pixel, solo cookies técnicas esenciales
 *  - Link "Configurar cookies" en footer para cambiar preferencias
 *  - Sin dependencias externas
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'certilab_cookies_accepted';
  var EXPIRY_DAYS = 365;
  var PIXEL_ID = '1271893388238243';

  /* ── Util: leer elección previa ── */
  function getConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (data.expires && Date.now() > data.expires) {
        localStorage.removeItem(STORAGE_KEY);
        return null;
      }
      return data.choice; // 'all' | 'essential'
    } catch (e) {
      return null;
    }
  }

  /* ── Util: guardar elección ── */
  function setConsent(choice) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        choice: choice,
        timestamp: Date.now(),
        expires: Date.now() + EXPIRY_DAYS * 24 * 60 * 60 * 1000
      }));
      console.log('Cookies: preferencia guardada → ' + choice);
    } catch (e) { /* storage no disponible */ }
  }

  /* ── Cargar Meta Pixel ── */
  function loadMetaPixel() {
    if (window.fbq) {
      console.log('Cookies: Meta Pixel ya estaba cargado');
      return;
    }
    try {
      !function(f,b,e,v,n,t,s) {
        if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s);
      }(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', PIXEL_ID);
      fbq('track', 'PageView');
      console.log('Cookies: Meta Pixel cargado (ID ' + PIXEL_ID + ')');
    } catch (e) {
      console.warn('Cookies: Meta Pixel no se ha podido cargar:', e);
    }
  }

  /* ── Construir banner en el DOM ── */
  function buildBanner() {
    // Evitar duplicado
    if (document.getElementById('cookie-banner')) return;

    var banner = document.createElement('div');
    banner.id = 'cookie-banner';
    banner.setAttribute('role', 'alert');
    banner.setAttribute('aria-live', 'polite');
    banner.innerHTML =
      '<div class="cookie-banner-inner">' +
        '<p class="cookie-banner-text">' +
          'Utilizamos cookies técnicas esenciales para el funcionamiento del sitio y cookies analíticas (Meta Pixel) para medir resultados. ' +
          'Puedes aceptar todas o solo las técnicas. ' +
          '<a href="/cookies.html">Más info</a>' +
        '</p>' +
        '<div class="cookie-banner-actions">' +
          '<button class="cookie-btn cookie-btn--secondary" id="cookies-essential">Solo técnicas</button>' +
          '<button class="cookie-btn cookie-btn--primary" id="cookies-all">Aceptar todas</button>' +
        '</div>' +
      '</div>';

    document.body.insertBefore(banner, document.body.firstChild);

    // Forzar reflow y mostrar con fade in
    banner.style.display = 'block';
    banner.style.opacity = '1';

    // Eventos
    document.getElementById('cookies-all').addEventListener('click', function () {
      setConsent('all');
      removeBanner();
      loadMetaPixel();
      console.log('Cookies: aceptadas todas');
    });

    document.getElementById('cookies-essential').addEventListener('click', function () {
      setConsent('essential');
      removeBanner();
      console.log('Cookies: solo técnicas');
    });
  }

  /* ── Eliminar banner con fadeOut ── */
  function removeBanner() {
    var banner = document.getElementById('cookie-banner');
    if (!banner) return;
    banner.style.opacity = '0';
    banner.style.transition = 'opacity 0.3s ease';
    setTimeout(function () {
      if (banner.parentNode) banner.parentNode.removeChild(banner);
    }, 350);
  }

  /* ── Inyectar link "Configurar cookies" en el footer ── */
  function injectConfigLink() {
    var footerLegal = document.querySelector('.footer-legal ul');
    if (!footerLegal) return;
    // Evitar duplicados
    if (document.getElementById('cookies-config-link')) return;

    var li = document.createElement('li');
    var link = document.createElement('a');
    link.id = 'cookies-config-link';
    link.href = '#';
    link.className = 'footer-cookies-config';
    link.textContent = 'Configurar cookies';
    link.addEventListener('click', function (e) {
      e.preventDefault();
      // Resetear consentimiento y mostrar banner
      localStorage.removeItem(STORAGE_KEY);
      console.log('Cookies: preferencias reseteadas, mostrando banner');
      buildBanner();
    });
    li.appendChild(link);
    footerLegal.appendChild(li);
  }

  /* ── Init ── */
  function init() {
    var consent = getConsent();

    if (consent === null) {
      // Sin decisión previa → mostrar banner
      console.log('Cookies: sin preferencia previa, mostrando banner');
      buildBanner();
    } else if (consent === 'all') {
      // Ya aceptó todas → cargar pixel directamente
      console.log('Cookies: preferencia "all" existente, cargando Pixel');
      loadMetaPixel();
    } else {
      console.log('Cookies: preferencia "essential" existente, sin Pixel');
    }

    // Inyectar link de configuración en footer
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', injectConfigLink);
    } else {
      injectConfigLink();
    }
  }

  // Arrancar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();