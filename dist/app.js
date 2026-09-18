(() => {
  'use strict';

  const FEDERAL_FACILITIES_URL = 'https://ftp.maps.canada.ca/pub/statcan_statcan/Health-care-facilities_Etablissement-de-sante/ODHF_BDOES/odhf_bdoes_v1.csv';
  const VANCOUVER_BOUNDS = [[49.198, -123.265], [49.318, -123.015]];
  const number = new Intl.NumberFormat('en-CA');

  // Geometry is intentionally simplified for planning interaction, not cadastral use.
  const sectorGeometry = {
    'Downtown Vancouver': { c:[49.282,-123.116], p:[[49.274,-123.134],[49.291,-123.134],[49.294,-123.106],[49.278,-123.099]] },
    'West End': { c:[49.286,-123.135], p:[[49.276,-123.148],[49.295,-123.143],[49.292,-123.127],[49.278,-123.126]] },
    'Fairview': { c:[49.263,-123.130], p:[[49.255,-123.147],[49.272,-123.146],[49.271,-123.112],[49.253,-123.112]] },
    'Downtown Eastside': { c:[49.282,-123.101], p:[[49.274,-123.111],[49.291,-123.108],[49.289,-123.090],[49.276,-123.089]] },
    'Strathcona': { c:[49.274,-123.088], p:[[49.266,-123.099],[49.280,-123.096],[49.281,-123.073],[49.267,-123.073]] },
    'Grandview-Woodlands': { c:[49.273,-123.066], p:[[49.261,-123.077],[49.291,-123.077],[49.290,-123.046],[49.260,-123.047]] },
    'Cedar Cottage': { c:[49.248,-123.070], p:[[49.236,-123.089],[49.260,-123.089],[49.260,-123.052],[49.236,-123.052]] },
    'Hastings-Sunrise': { c:[49.281,-123.039], p:[[49.260,-123.053],[49.294,-123.052],[49.294,-123.023],[49.259,-123.024]] },
    'Renfrew-Collingwood': { c:[49.242,-123.041], p:[[49.218,-123.058],[49.260,-123.059],[49.260,-123.022],[49.218,-123.023]] },
    'Shaughnessy / Arbutus / Kerrisdale': { c:[49.236,-123.151], p:[[49.211,-123.170],[49.258,-123.169],[49.258,-123.134],[49.211,-123.135]] },
    'West Point Grey / Dunbar': { c:[49.248,-123.198], p:[[49.218,-123.224],[49.275,-123.222],[49.275,-123.166],[49.217,-123.169]] },
    'UBC': { c:[49.258,-123.243], p:[[49.226,-123.265],[49.283,-123.264],[49.283,-123.220],[49.226,-123.222]] },
    'Kitsilano': { c:[49.268,-123.170], p:[[49.257,-123.200],[49.281,-123.198],[49.280,-123.145],[49.257,-123.145]] },
    'Kensington': { c:[49.224,-123.084], p:[[49.208,-123.105],[49.239,-123.105],[49.239,-123.064],[49.208,-123.063]] },
    'Mount Pleasant': { c:[49.259,-123.098], p:[[49.239,-123.113],[49.272,-123.112],[49.273,-123.087],[49.239,-123.087]] },
    'South Cambie / Riley Park': { c:[49.236,-123.120], p:[[49.211,-123.137],[49.255,-123.137],[49.254,-123.102],[49.211,-123.102]] },
    'Killarney': { c:[49.216,-123.043], p:[[49.199,-123.063],[49.235,-123.063],[49.235,-123.022],[49.200,-123.023]] },
    'Oakridge / Marpole': { c:[49.215,-123.128], p:[[49.199,-123.149],[49.233,-123.148],[49.232,-123.104],[49.198,-123.104]] },
    'Sunset': { c:[49.220,-123.091], p:[[49.199,-123.107],[49.239,-123.106],[49.239,-123.083],[49.199,-123.083]] },
    'Victoria-Fraserview': { c:[49.216,-123.066], p:[[49.199,-123.084],[49.238,-123.084],[49.238,-123.052],[49.199,-123.053]] }
  };

  const nameCrosswalk = {
    'Northeast False Creek': { code:'1622', name:'Strathcona', region:'CHA 2 (Mid-East)' },
    'Downtown Eastside': { code:'1621', name:'Downtown Eastside', region:'CHA 2 (Mid-East)' },
    'Grandview-Woodland': { code:'1623', name:'Grandview-Woodlands', region:'CHA 2 (Mid-East)' },
    'Shaughnessy/Arbutus Ridge/Kerrisdale': { name:'Shaughnessy / Arbutus / Kerrisdale' },
    'West Point Grey/Dunbar-Southlands': { name:'West Point Grey / Dunbar' },
    'University of British Columbia': { name:'UBC' },
    'South Cambie/Riley Park': { name:'South Cambie / Riley Park' }
  };

  const fallbackFacilities = [
    ['Vancouver General Hospital','Hospitals',49.261616,-123.1239113],
    ['VGH — Diamond Health Care Centre','Hospitals',49.261187,-123.125655],
    ['UBC Hospital — Koerner Pavilion','Hospitals',49.26425,-123.24543],
    ['GF Strong Rehabilitation Centre','Hospitals',49.24531,-123.12318],
    ['Mount Saint Joseph Hospital','Hospitals',49.257699,-123.096358],
    ['Mid-Main Community Health Centre','Ambulatory health care services',49.249493,-123.100611],
    ['Three Bridges Community Health Centre','Ambulatory health care services',49.27596,-123.12967],
    ['Downtown Community Health Centre','Ambulatory health care services',49.28103,-123.09861],
    ['Raven Song Community Health Centre','Ambulatory health care services',49.25742,-123.10118],
    ['South Community Health Centre','Ambulatory health care services',49.20968,-123.11636],
    ['Pender Community Health Centre','Ambulatory health care services',49.28022,-123.10419],
    ['Heatley Community Health Centre','Ambulatory health care services',49.28031,-123.08871]
  ].map((r,i)=>({id:`fallback-${i}`,name:r[0],type:r[1],lat:r[2],lng:r[3],source:'Verified local fallback'}));

  let sectors = [], facilities = [], selectedKey = 'all', map, zoneLayer, markerLayer;

  const $ = id => document.getElementById(id);
  const setText = (id, value) => { $(id).textContent = value; };

  function normalizeRow(row) {
    const mapped = nameCrosswalk[row.CH_SA_NAME] || {};
    const name = mapped.name || row.CH_SA_NAME;
    return {
      CMNTY_HLTH_SERV_AREA_CODE: mapped.code || row.CH_SA_CODE,
      CMNTY_HLTH_SERV_AREA_NAME: name,
      SOURCE_CHSA_NAME: row.CH_SA_NAME,
      CHSA_POPULATION_CENSUS: +row.CHSPOP_CEN,
      LONG_FORM_GNR: +row.LG_FRM_GNR / 100,
      AGE_GROUPS_ALL_TOTAL: +row.GRP_A_TTL,
      AGE_0_14_ALL_TOTAL: +row['0_14_A_TTL'],
      region: mapped.region || name,
      geometry: sectorGeometry[name]
    };
  }

  function parseCsv(text) {
    if (window.Papa) return Papa.parse(text, { header:true, skipEmptyLines:true }).data;
    const lines = text.trim().split(/\r?\n/), headers = lines.shift().split(',');
    return lines.map(line => Object.fromEntries(line.split(',').map((v,i)=>[headers[i],v])));
  }

  async function loadCensus() {
    const response = await fetch('data/BCHACHSAPO.csv');
    if (!response.ok) throw new Error('Local census extract unavailable');
    sectors = parseCsv(await response.text()).map(normalizeRow).filter(s=>s.geometry);
  }

  function isPublicPlanningFacility(row) {
    const name = (row.facility_name || '').toLowerCase();
    const type = row.odhf_facility_type || '';
    if (!['Hospitals','Ambulatory health care services'].includes(type)) return false;
    return /hospital|health cent|community health|vancouver coastal|rehabilitation/.test(name) && !/children|women|st\. paul|providence|cancer|medical clinic/.test(name);
  }

  async function loadFacilities() {
    try {
      const response = await fetch(FEDERAL_FACILITIES_URL, { mode:'cors' });
      if (!response.ok) throw new Error('Federal CDN unavailable');
      const rows = parseCsv(await response.text());
      const filtered = rows.filter(row =>
        String(row.province || '').trim().toUpperCase() === 'BC' &&
        String(row.city || '').trim().toLowerCase() === 'vancouver' &&
        Number.isFinite(+row.latitude) && Number.isFinite(+row.longitude) &&
        isPublicPlanningFacility(row)
      );
      const seen = new Set();
      facilities = filtered.filter(row => {
        const key = `${(+row.latitude).toFixed(4)}|${(+row.longitude).toFixed(4)}`;
        if (seen.has(key)) return false; seen.add(key); return true;
      }).map(row=>({id:`f-${row.index}`,name:titleCase(row.facility_name),type:row.odhf_facility_type,lat:+row.latitude,lng:+row.longitude,source:'Statistics Canada ODHF'}));
      if (facilities.length < 4) throw new Error('Insufficient federal facility records');
      setPipeline(`Live federal pipeline · ${facilities.length} Vancouver records`, true);
    } catch (error) {
      facilities = fallbackFacilities;
      setPipeline(`Local fallback · ${facilities.length} verified records`, true);
    }
  }

  function titleCase(text){ return String(text).replace(/\b\w/g,c=>c.toUpperCase()).replace(/\bVgh\b/g,'VGH').replace(/\bUbc\b/g,'UBC'); }
  function setPipeline(text, ready){ $('pipelineStatus').classList.toggle('ready',ready); $('pipelineStatus').querySelector('span').textContent=text; }

  function initMap() {
    if (!window.L) { $('map').innerHTML='<div style="padding:2rem">Map library could not load. Metrics and sector controls remain available.</div>'; return; }
    map = L.map('map',{zoomControl:false,minZoom:11,maxBounds:[[49.17,-123.31],[49.34,-122.98]],maxBoundsViscosity:1}).fitBounds(VANCOUVER_BOUNDS);
    L.control.zoom({position:'bottomright'}).addTo(map);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap &copy; CARTO'}).addTo(map);
    zoneLayer = L.layerGroup().addTo(map); markerLayer = L.layerGroup().addTo(map);
    renderMapLayers();
  }

  function priorityScore(s) {
    const youth = s.AGE_0_14_ALL_TOTAL / s.AGE_GROUPS_ALL_TOTAL * 100;
    return Math.round(Math.min(100, 25 + youth * 2.3 + s.LONG_FORM_GNR * 180));
  }

  function renderMapLayers() {
    if (!map) return;
    zoneLayer.clearLayers(); markerLayer.clearLayers();
    sectors.forEach(s=>{
      const isSelected = selectedKey === s.CMNTY_HLTH_SERV_AREA_NAME || (selectedKey === 'CHA 2 (Mid-East)' && s.region === selectedKey);
      const polygon = L.polygon(s.geometry.p,{color:isSelected?'#00a6a6':'#54788a',weight:isSelected?3:1,fillColor:isSelected?'#00a6a6':'#8db3bd',fillOpacity:isSelected?.30:.10});
      polygon.bindTooltip(`<strong>${s.CMNTY_HLTH_SERV_AREA_NAME}</strong><br>${(s.LONG_FORM_GNR*100).toFixed(1)}% GNR`,{sticky:true});
      polygon.on('click',()=>selectArea(s.CMNTY_HLTH_SERV_AREA_NAME,true)); polygon.addTo(zoneLayer);
    });
    facilities.forEach(f=>{
      if (!insideVancouver(f)) return;
      const sector = nearestSector(f), cls = f.type === 'Hospitals'?'hospital':'clinic';
      const icon = L.divIcon({className:'facility-marker',html:`<span class="facility-pin ${cls}"></span>`,iconSize:[24,30],iconAnchor:[12,28]});
      const marker=L.marker([f.lat,f.lng],{icon,title:f.name});
      marker.bindPopup(`<div class="popup-title">${escapeHtml(f.name)}</div><div class="popup-type">${f.type === 'Hospitals'?'Acute / hospital':'Ambulatory / community care'}</div><div class="popup-stat"><span>Nearest CHSA</span><strong>${sector.CMNTY_HLTH_SERV_AREA_NAME}</strong></div><div class="popup-stat"><span>Pediatric index</span><strong>${pediatricPct([sector]).toFixed(1)}%</strong></div><button class="popup-link" data-sector="${escapeHtml(sector.CMNTY_HLTH_SERV_AREA_NAME)}">Open sector</button>`);
      marker.on('popupopen',e=>{ const btn=e.popup.getElement().querySelector('.popup-link'); if(btn) btn.onclick=()=>selectArea(btn.dataset.sector,true); });
      marker.on('click',()=>selectArea(sector.CMNTY_HLTH_SERV_AREA_NAME,false,f)); marker.addTo(markerLayer);
    });
  }

  function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function insideVancouver(f){return f.lat>=VANCOUVER_BOUNDS[0][0]&&f.lat<=VANCOUVER_BOUNDS[1][0]&&f.lng>=VANCOUVER_BOUNDS[0][1]&&f.lng<=VANCOUVER_BOUNDS[1][1];}
  function nearestSector(f){return sectors.reduce((a,s)=>distance(f,s.geometry.c)<distance(f,a.geometry.c)?s:a,sectors[0]);}
  function distance(f,c){return Math.hypot(f.lat-c[0],(f.lng-c[1])*.7);}

  function selectedSectors(){ if(selectedKey==='all') return sectors; if(selectedKey==='CHA 2 (Mid-East)') return sectors.filter(s=>s.region===selectedKey); return sectors.filter(s=>s.CMNTY_HLTH_SERV_AREA_NAME===selectedKey); }
  function pediatricPct(rows){const total=rows.reduce((n,s)=>n+s.AGE_GROUPS_ALL_TOTAL,0);return total?rows.reduce((n,s)=>n+s.AGE_0_14_ALL_TOTAL,0)/total*100:0;}
  function weightedGnr(rows){const total=rows.reduce((n,s)=>n+s.CHSA_POPULATION_CENSUS,0);return total?rows.reduce((n,s)=>n+s.LONG_FORM_GNR*s.CHSA_POPULATION_CENSUS,0)/total*100:0;}
  function facilitiesFor(rows){const names=new Set(rows.map(s=>s.CMNTY_HLTH_SERV_AREA_NAME));return facilities.filter(f=>names.has(nearestSector(f).CMNTY_HLTH_SERV_AREA_NAME));}

  function selectArea(key, zoom=false, facility=null){
    selectedKey=key; const rows=selectedSectors(); updatePanel(rows,facility); renderSectorList(); renderMapLayers();
    if(map&&zoom){const shapes=rows.map(s=>s.geometry.p).flat(); map.fitBounds(L.latLngBounds(shapes),{padding:[30,30],maxZoom:14});}
  }

  function allocation(rows){
    const youth=pediatricPct(rows),gnr=weightedGnr(rows);
    const pediatric=Math.round(Math.min(42,Math.max(22,18+youth*1.15)));
    const outreach=Math.round(Math.min(28,Math.max(8,4+gnr*1.55)));
    return {pediatric,outreach,core:100-pediatric-outreach};
  }

  function updatePanel(rows,facility){
    const pop=rows.reduce((n,s)=>n+s.CHSA_POPULATION_CENSUS,0), youth=pediatricPct(rows), gnr=weightedGnr(rows), local=facilitiesFor(rows), alloc=allocation(rows);
    const label=selectedKey==='all'?'City of Vancouver':selectedKey;
    setText('selectionTitle',facility?facility.name:label);
    setText('selectionMeta',facility?`${facility.type} · nearest sector: ${label}`:`${rows.length} CHSA${rows.length===1?'':'s'} · ${selectedKey==='CHA 2 (Mid-East)'?'unified priority region':'planning selection'}`);
    setText('mapContext',label); setText('populationKpi',number.format(pop)); setText('pediatricKpi',`${youth.toFixed(1)}%`);
    setText('pediatricDetail',`${number.format(rows.reduce((n,s)=>n+s.AGE_0_14_ALL_TOTAL,0))} residents age 0–14`);
    setText('gnrKpi',`${gnr.toFixed(1)}%`); setText('facilityKpi',number.format(local.length)); setText('facilityDetail',local.length===1?'Mapped facility nearby':'Mapped facilities nearby');
    let level, text, icon;
    if(gnr>10){level='high';icon='!';text='Resource models are unstable due to high census non-response in this sector.';setText('riskLabel','HIGH DATA BLINDSPOT RISK');}
    else if(gnr>=5){level='medium';icon='⚠';text='Validate priority estimates with local service-use data and targeted community outreach.';setText('riskLabel','MEDIUM RISK');}
    else{level='low';icon='✓';text='Census response supports a reliable baseline for local planning.';setText('riskLabel','LOW RISK / RELIABLE BASELINE');}
    $('riskCard').className=`risk-card ${level}`;setText('riskIcon',icon);setText('riskText',text);
    setText('pediatricBudget',`${alloc.pediatric}%`);setText('outreachBudget',`${alloc.outreach}%`);setText('coreBudget',`${alloc.core}%`);
    $('pediatricBar').style.width=`${alloc.pediatric}%`;$('outreachBar').style.width=`${alloc.outreach}%`;$('coreBar').style.width=`${alloc.core}%`;
    setText('recommendation',`Strategic Allocation: Distribute ${alloc.pediatric}% of localized public health funding to Pediatric Clinical Staff and ${alloc.outreach}% to Data Verification/Community Outreach Mobile Teams. Retain ${alloc.core}% for core operations and adult care.`);
  }

  function renderSectorList(){
    const groups=[{key:'CHA 2 (Mid-East)',name:'CHA 2 (Mid-East)',rows:sectors.filter(s=>s.region==='CHA 2 (Mid-East)')},...sectors.filter(s=>s.region!=='CHA 2 (Mid-East)').map(s=>({key:s.CMNTY_HLTH_SERV_AREA_NAME,name:s.CMNTY_HLTH_SERV_AREA_NAME,rows:[s]}))];
    groups.sort((a,b)=>avgPriority(b.rows)-avgPriority(a.rows)); setText('sectorCount',`${groups.length} planning zones`);
    $('sectorList').innerHTML=groups.map(g=>{const score=avgPriority(g.rows),gnr=weightedGnr(g.rows);return `<button class="sector-btn ${selectedKey===g.key?'active':''}" data-key="${escapeHtml(g.key)}"><span class="priority-score" style="background:${priorityColor(score)}">${score}</span><span class="sector-name">${escapeHtml(g.name)}<span class="sector-sub">${g.rows.length>1?g.rows.map(r=>r.CMNTY_HLTH_SERV_AREA_CODE).join(' · '):g.rows[0].CMNTY_HLTH_SERV_AREA_CODE}</span></span><span class="sector-gnr">${gnr.toFixed(1)}% GNR</span><span class="sector-arrow">›</span></button>`}).join('');
    $('sectorList').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>selectArea(b.dataset.key,true)));
  }
  function avgPriority(rows){return Math.round(rows.reduce((n,s)=>n+priorityScore(s),0)/rows.length)}
  function priorityColor(score){if(score>=80)return'#d64c4c';if(score>=70)return'#d47b31';if(score>=60)return'#087b82';if(score>=50)return'#2e9298';return'#6c9da5'}

  function registerWebMcp(){
    const context=document.modelContext;
    if(!context?.registerTool)return;
    const validAreas=['all','CHA 2 (Mid-East)',...sectors.map(s=>s.CMNTY_HLTH_SERV_AREA_NAME)];
    try{
      void Promise.resolve(context.registerTool({
        name:'select_vancouver_planning_area',
        title:'Select Vancouver planning area',
        description:'Select a Vancouver CHSA or CHA 2 (Mid-East) and recalculate the visible vulnerability and funding indicators.',
        inputSchema:{type:'object',properties:{area:{type:'string',enum:validAreas}},required:['area'],additionalProperties:false},
        annotations:{readOnlyHint:false,untrustedContentHint:false},
        execute(input){
          if(!input||!validAreas.includes(input.area))throw new Error('Unknown Vancouver planning area');
          selectArea(input.area,true);
          const rows=selectedSectors();
          return {area:input.area,pediatricVulnerabilityPct:+pediatricPct(rows).toFixed(1),longFormGnrPct:+weightedGnr(rows).toFixed(1),allocation:allocation(rows)};
        }
      })).catch(()=>{});
    }catch(error){console.debug('WebMCP unavailable',error);}
  }

  async function boot(){
    try{await loadCensus();await loadFacilities();initMap();renderSectorList();updatePanel(sectors);registerWebMcp();}
    catch(error){setPipeline('Data initialization issue',false);console.error(error);}
    $('resetView').addEventListener('click',()=>{selectedKey='all';updatePanel(sectors);renderSectorList();renderMapLayers();if(map)map.fitBounds(VANCOUVER_BOUNDS);});
  }
  boot();
})();
