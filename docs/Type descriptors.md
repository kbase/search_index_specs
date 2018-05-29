# Structure of type descriptors in Search (RESKE) configuration  

Type descriptor is configuration file RESKE Search Service defining how to index different objects (or parts of objects) stored in Workspace Service. By indexing it’s meant the way how to prepare object so that it could be looked up by values (or words of string values in case of full-text index) stored inside different elements of given object (for instance array items or properties of structures).   

## General format of type descriptor  

Type descriptor is formatted as JSON document and includes these main parameters (some of that are optional): 
* **global-object-type** - name of type of indexed entity this type descriptor is designed for. This type is supposed to be used in Search API to specify filter on particular object type. 
* **ui-type-name** - (optional) title of type used by UI to show as type filter or in search results. If this property is not set then name from `global-object-type` is used. 
* **storage-type** - code of storage (or data source). It’s mostly for future usages and should be set to default value (“WS” meaning Workspace Service).  
* **storage-object-type** - type of object in storage (or data source). 
* **inner-sub-type** - (optional) specification of sub-type corresponding to parts of object (for instance “feature” structures inside genome object). This property should be specified only for cases of indexing parts of object rather than whole object. It’s used to differentiate between several sub-types inside same object. For instance you may have “rna” and “protein” items of genome indexed differently. Value of this property is included as part of GUID defined for indexed sub-objects (see “GUID structure” section). 
* **path-to-sub-objects** - (optional) JSON-path defining how to find sub-objects inside object. This property should be specified only for cases of indexing parts of object rather than whole object. Such JSON-path may include slashes (“/”) pointing to places in JSON object where we should go deeper in order to find necessary sub-objects. Elements between slashes correspond to names of fields in structures or positions in arrays. Special star elements are treated as any field in structure (“*”) or any position in array (“[*]”). 
* **indexing-rules** - list of rules defining how to transform elements of sub-object into indexed keywords (that you will be able to search by). Main idea here is that not all content of objects (sub-objects) is supposed to be indexed. Instead, we index only those elements defined in these indexing rules. See next section for details. 
* **primary-key-path** - (not used) for future usages (related to `relation-rules` property). 
* **relation-rules** - (not used) for future usages (it’s supposed to be a way for extraction of relationships for Relation Engine from object content).   Indexing rules in type descriptor  Each indexing rule should be defined in order to form key-value pair based on some content in object (sub-object) or based on key-value pair formed by another indexing rule. Here is list of properties in JSON structure of each indexing rule: 
* **path** - (optional) JSON-path inside [sub-]object pointing to value for indexing as keyword. Not used if `derived-key` is set to true. As usual “*” and “[*]” could be used in JSON-path in order to collect more than one value for this keyword (in Elasticsearch any keyword value is treated as a list). As Gavin reminded there is support for special JSON-path item called “{size}”. In this case size of array or map is included into object content instead of real data. 
* **keyword-type** - (optional) Elasticsearch type of keyword (in case neither `keyword-type` or `full-text` is defined **keyword** type is used in Elasticsearch). **string** value also corresponds to **keyword** type is used in Elasticsearch. 
* **full-text** - (optional, boolean) value true is alternative to **keyword-type**. In this case **text** type is used in Elasticsearch (which means full-text mode for this keyword). Default value is false. 
* **key-name** - (optional) name of key for keyword. If not set then first item between slashes in `path` is used. 
* **transform** - (optional) transformation applied to values coming from [sub-]object or source keyword. Value of this property has format of <transform>[.<ret-prop>], where second part including dot is optional and used in some of transformations. Here is the list of currently supported transformations:  
    * **location**: transforms KBase location tuple ([contig_id, start, strand, length]) to one of **contig_id**, **start**, **strand**, **length** or **stop** values corresponding to <ret-prop> part of transformation. 
    * **values**: transforms object or array of values to strings of all primitive components. 
    * **string**: transforms value to string (String.valueOf function). 
    * **integer**: transforms value to Integer (Integer.parseInt of String.valueOf). 
    * **guid**: transforms value containing reference to WS object into GUID (see `target-object-type` and `subobject-id-key` properties for details). 
    * **lookup**: transforms value containing GUID into keyword loaded from content of external object referenced by this GUID. External keyword name is defined in <ret-prop> part of transformation. 
* **derived-key** - (optional, boolean) flag saying that this rule defines keyword formed based on another (source) keyword which is set in `source-key`. Default value is false (which means that it’s not derived keyword and we use **path** instead). 
* **source-key** - (optional) defines source keyword providing value instead of `path` property. Is used only if `derived-key` is set to true. This property works only if **derived-key** is set to true. 
* **target-object-type** - (optional) can be defined for derived keyword only. Is used in `guid` transform mode only. This property provides type descriptor name of [sub-]object where resulting GUID points to. In addition to validation purpose target type helps form sub-object part of GUID where we need to know not only sub-object ID (coming from `subobject-id-key`) but also sub-object inner type which is extracted from this target type descriptor. 
* **subobject-id-key** - (optional) can be defined for derived keyword only. Works together with `target-object-type`. Is used in `guid` transform mode only. This property points to keyword providing value for sub-object inner ID in order to construct full GUID for sub-object. 
* **not-indexed**- (optional, boolean, default=false) indicates that value should be included into extracted part of object data but not present as indexed keyword
* **from-parent** - (optional, boolean, default=false) indicates that value is extracted from parent document (main object) rather that from sub-object. 
* **optional-default-value** - (optional) value which is used for keyword in case resulting array of values extracted from [sub-]object document is empty. 
* **ui-name** - name of keyword displayed by UI. 
* **ui-link-key** - (optional) pointer to paired keyword coupled with given one providing GUID for making clickable URL for value provided. Example: one keyword called “Genome name” may have “ui-link-key” pointer to another keyword called “Genome GUID” so that Search UI will use values of these two keywords in order to produce clickable link showing genome name (coming from one keyword) and redirecting you to landing page of given genome based on GUID (coming from another keyword). 
* **ui-hidden** - (optional, boolean, default=false) indicates that particular keyword is not supposed to be visible via UI though it could be used in API search queries.   

## Structure of GUID (Global User ID)

GUID is an attempt of generalization for space of Workspace Service references. It was designed to support other Data Sources (like NCBI Taxonomy or variety of Ontologies). That is why there is DataSource prefix there. Another reason of inventing it is to support sub-object references (or some unified way of identification of sub-objects inside main object (like features in genome). Here is formal structure of GUID string:  

`{DataSource}:[{AccessGroupID}/]{ObjectID-or-name}[/{version}][:{inner-type}/{sub-ID-or-name}]`  

In these terms ID looking like GO:1234567 fits into GUID schema as well. In this case “GO” means Data Source code, and 1234567 is object ID. Another example of GUIDs with sub-IDs is features. In this case GUID may look like `WS:21206/12/1:feature/Agm123005`, where “WS” is default Workspace code followed by ws-ref followed by “feature” (inner type inside Genome) and then particular feature sub-ID. 