<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--
  <xsl:strip-space elements="*"/>
-->
<xsl:output indent="yes"/>

<xsl:template match="/">
    <device schemaVersion="1.1" xmlns:xs="http://www.w3.org/2001/XMLSchema-instance" xs:noNamespaceSchemaLocation="CMSIS-SVD.xsd">
      <xsl:apply-templates/>  
    </device>
</xsl:template>

<!--
<xsl:template match="ipxact:vendor">
  <vendor>
    <xsl:apply-templates select="vendor"/>  
  </vendor>
</xsl:template>
-->

</xsl:stylesheet>