<!-- 
// Copyright (c) 2005 - 2012 Accellera Systems Initiative Inc. 
// All rights reserved.
//
// THIS WORK FORMS PART OF A ACCELLERA SYSTEMS INITIATIVE SPECIFICATION.
// USE OF THESE MATERIALS ARE GOVERNED BY
// THE LEGAL TERMS AND CONDITIONS OUTLINED IN THE IPXACT
// SPECIFICATION DISCLAIMER AVAILABLE FROM
// www.accellera.org
//
// This source file is provided on an AS IS basis. The Accellera Systems Initiative disclaims 
// ANY WARRANTY EXPRESS OR IMPLIED INCLUDING ANY WARRANTY OF
// MERCHANTABILITY AND FITNESS FOR USE FOR A PARTICULAR PURPOSE. 
// The user of the source file shall indemnify and hold The Accellera Systems Initiative
// harmless from any damages or liability arising out of the use thereof or the 
// performance or implementation or partial implementation of the schema.
  -->

<!--
// Description :  from1.5_to_1685_2009.xsl
// XSL transform to go from the 1.5 version to the 1685-2009 version of the Schema
// Author: The Accellera System Initiative IP-XACT Schema Working Group
// Date: July 5, 2012
-->
  
<xsl:stylesheet version="1.0" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xmlns:spirit15="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5"
	xmlns:kactus2="http://funbase.cs.tut.fi/">

<xsl:param name="namespace" select="'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009'"
xmlns:kactus2="http://funbase.cs.tut.fi/"/>

<xsl:strip-space elements="*"/>
<xsl:output method="xml" indent="yes"/>

<!-- Process the document node. -->
<xsl:template match="/">
  <xsl:apply-templates select="comment() | processing-instruction()"/>
  <xsl:apply-templates select="*"/>
</xsl:template>

<xsl:template match="*">
  <xsl:element name="{name()}" namespace="{namespace-uri()}">
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>

<!-- Copy comments, pi's and text. -->
<xsl:template match="comment() | processing-instruction()">
  <xsl:copy>
    <xsl:apply-templates/>
  </xsl:copy><xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="@*">
  <xsl:attribute name="{name()}" namespace="{namespace-uri()}">
    <xsl:value-of select="."/>
  </xsl:attribute>
</xsl:template>

<xsl:template match="/spirit15:*">
  <xsl:element name="spirit:{local-name()}" namespace="{$namespace}">
    <xsl:for-each select="namespace::*">
      <xsl:if test="not(.='http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5')">
        <xsl:copy/>
      </xsl:if>
    </xsl:for-each>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>

<xsl:template match="@xsi:schemaLocation">
  <xsl:attribute name="xsi:schemaLocation">
    <xsl:text>http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009 http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009/index.xsd</xsl:text>
  </xsl:attribute>
</xsl:template>

<xsl:template match="spirit15:*">
  <xsl:element name="spirit:{local-name()}" namespace="{$namespace}">
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>

<!-- The attributes need to be handled a little differently, to avoid confusing the 
    processor, the namespaceURI should not be explicitly defined -->
<xsl:template match="@spirit15:*">
  <xsl:attribute name="spirit:{local-name()}" namespace="{$namespace}">
    <xsl:value-of select="."/>
  </xsl:attribute>
</xsl:template>

</xsl:stylesheet>