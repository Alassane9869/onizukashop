import os

filepath = os.path.join('templates', 'shop', 'product_detail.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize CRLF to LF temporarily for matching
is_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')

old_event_anchor = """         this.whatsappModalOpen = false;
       }
     }">"""

new_event_anchor = """         this.whatsappModalOpen = false;
       }
     }"
     @open-product-whatsapp.window="whatsappModalOpen = true">"""

if old_event_anchor in content_lf:
    content_lf = content_lf.replace(old_event_anchor, new_event_anchor, 1)
    print("1. Added window event listener.")
else:
    print("1. old_event_anchor not found, maybe already replaced.")

old_modal = """  <div \n    x-show="whatsappModalOpen" \n    x-cloak\n    class="fixed inset-0 z-50 overflow-y-auto" """
old_modal_trim = """  <div 
    x-show="whatsappModalOpen" 
    x-cloak
    class="fixed inset-0 z-50 overflow-y-auto" """

# check without trailing space
old_modal_exact = """  <div 
    x-show="whatsappModalOpen" 
    x-cloak
    class="fixed inset-0 z-50 overflow-y-auto\""""

new_modal_exact = """  <div 
    x-show="whatsappModalOpen" 
    x-cloak
    style="display: none;"
    class="fixed inset-0 z-50 overflow-y-auto\""""

if old_modal_exact in content_lf:
    content_lf = content_lf.replace(old_modal_exact, new_modal_exact, 1)
    print("2. Added display:none to modal.")
else:
    print("2. old_modal_exact not found.")

old_tail = """</div>

<!-- Barre d'Action Mobile Dédiée (iOS iPhone Dock Calibre Apple) -->
{% block bottom_nav %}
{% if product.is_in_stock %}
<div class="lg:hidden ios-nav-dock px-3 py-2 flex items-center justify-between gap-2 shadow-[0_-8px_30px_rgba(0,0,0,0.06)] border-t border-black/[0.06] bg-white/95 backdrop-blur-2xl">
  <div class="leading-tight select-none">
    <div class="flex items-center gap-1">
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
      <p class="text-[10px] text-neutral-400 font-bold uppercase tracking-wider">En stock</p>
    </div>
    <p class="font-display text-sm sm:text-base font-black text-neutral-900 tracking-tight font-mono">
      {{ product.price|floatformat:0|intcomma }} <span class="font-sans text-[11px] font-bold text-neutral-400">FCFA</span>
    </p>
  </div>

  <div class="flex items-center gap-2">
    <!-- Bouton WhatsApp Mobile Compact -->
    <button 
      type="button" 
      @click="whatsappModalOpen = true"
      class="h-10 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-sm shrink-0"
      title="Commander sur WhatsApp"
    >
      <svg class="w-4 h-4 fill-white" viewBox="0 0 24 24">
        <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.588-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.299.144.347.491 1.2.534 1.287.043.087.072.188.014.303-.058.116-.087.188-.173.289l-.26.303c-.087.087-.179.182-.077.357.101.174.45 1.054 1.325 1.833.687.612 1.267.801 1.447.888.181.087.289.073.397-.051.108-.124.462-.538.585-.722.123-.184.246-.153.411-.092.166.061 1.052.496 1.233.587.181.091.303.136.347.212.043.076.043.439-.101.844z"/>
      </svg>
      <span>WhatsApp</span>
    </button>

    <!-- Bouton Panier Mobile -->
    <form 
      method="post" 
      action="{% url 'orders:cart_add' product.pk %}"
      hx-post="{% url 'orders:cart_add' product.pk %}"
      hx-swap="none"
      class="shrink-0"
    >
      {% csrf_token %}
      <input type="hidden" name="quantity" :value="qty">
      <button 
        type="submit" 
        class="h-10 px-3.5 rounded-xl bg-amber-500 hover:bg-amber-600 active:bg-amber-700 text-slate-950 font-bold text-xs shadow-sm flex items-center justify-center gap-1.5 transition-all cursor-pointer"
      >
        <svg class="w-4 h-4 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/></svg>
        <span>Ajouter</span>
      </button>
    </form>
  </div>
</div>
{% endif %}
{% endblock %}

{% endblock %}"""

new_tail = """</div>
{% endblock %}

<!-- Barre d'Action Mobile Dédiée (iOS iPhone Dock Calibre Apple) -->
{% block bottom_nav %}
{% if product.is_in_stock %}
<div class="lg:hidden ios-nav-dock px-3.5 py-2.5 flex items-center justify-between gap-3 shadow-[0_-8px_30px_rgba(0,0,0,0.08)] border-t border-slate-200/80 bg-white/95 backdrop-blur-2xl z-50 fixed bottom-0 left-0 right-0"
     x-data="{ mobileQty: 1 }">
  <div class="leading-tight select-none">
    <div class="flex items-center gap-1">
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
      <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">En stock Bamako</p>
    </div>
    <p class="font-heading text-sm sm:text-base font-black text-slate-900 tracking-tight font-mono">
      {{ product.current_price|floatformat:0|intcomma }} <span class="font-sans text-[11px] font-bold text-slate-400">FCFA</span>
    </p>
  </div>

  <div class="flex items-center gap-2">
    <!-- Bouton WhatsApp Mobile Direct -->
    <button 
      type="button" 
      @click="$dispatch('open-product-whatsapp')"
      class="h-10 px-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 text-white font-bold text-xs flex items-center justify-center gap-1.5 transition shadow-sm shrink-0 cursor-pointer"
      title="Commander sur WhatsApp"
    >
      <svg class="w-4 h-4 fill-white" viewBox="0 0 24 24">
        <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.588-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.299.144.347.491 1.2.534 1.287.043.087.072.188.014.303-.058.116-.087.188-.173.289l-.26.303c-.087.087-.179.182-.077.357.101.174.45 1.054 1.325 1.833.687.612 1.267.801 1.447.888.181.087.289.073.397-.051.108-.124.462-.538.585-.722.123-.184.246-.153.411-.092.166.061 1.052.496 1.233.587.181.091.303.136.347.212.043.076.043.439-.101.844z"/>
      </svg>
      <span>WhatsApp</span>
    </button>

    <!-- Bouton Panier Mobile -->
    <form 
      method="post" 
      action="{% url 'orders:cart_add' product.pk %}"
      hx-post="{% url 'orders:cart_add' product.pk %}"
      hx-swap="none"
      class="shrink-0"
    >
      {% csrf_token %}
      <input type="hidden" name="quantity" :value="mobileQty">
      <button 
        type="submit" 
        class="h-10 px-4 rounded-xl bg-amber-500 hover:bg-amber-600 active:bg-amber-700 text-slate-950 font-bold text-xs shadow-sm flex items-center justify-center gap-1.5 transition-all cursor-pointer"
      >
        <svg class="w-4 h-4 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/></svg>
        <span>Ajouter</span>
      </button>
    </form>
  </div>
</div>
{% endif %}
{% endblock %}"""

if old_tail in content_lf:
    content_lf = content_lf.replace(old_tail, new_tail, 1)
    print("3. Cleaned and separated bottom_nav block.")
else:
    print("3. old_tail not found.")

final_content = content_lf.replace('\n', '\r\n') if is_crlf else content_lf
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Done fixing product_detail.html!")
