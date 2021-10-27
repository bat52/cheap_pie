<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- 
// Copyright (c) 2005, 2006, 2007, 2008, 2009 The SPIRIT Consortium.  All rights reserved.
// www.spiritconsortium.org
//
// THIS WORK FORMS PART OF A SPIRIT CONSORTIUM SPECIFICATION.
// USE OF THESE MATERIALS ARE GOVERNED BY
// THE LEGAL TERMS AND CONDITIONS OUTLINED IN THE SPIRIT
// SPECIFICATION DISCLAIMER AVAILABLE FROM
// www.spiritconsortium.org
//
// This source file is provided on an AS IS basis. The SPIRIT Consortium disclaims 
// ANY WARRANTY EXPRESS OR IMPLIED INCLUDING ANY WARRANTY OF
// MERCHANTABILITY AND FITNESS FOR USE FOR A PARTICULAR PURPOSE. 
// The user of the source file shall indemnify and hold The SPIRIT Consortium harmless
// from any damages or liability arising out of the use thereof or the performance or
// implementation or partial implementation of the schema.
  -->
<!--
// Description :  from1.4_to1.5.xsl
// XSL transform to go from V1.4 version to V1.5 version of the Schema
// Author : SPIRIT Schema Working Group - Christophe Amerijckx
// Date:     March 9, 2009
     -->

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:spirit14="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.4" xmlns:kactus2="http://funbase.cs.tut.fi/">

<xsl:param name="namespace" select="'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5'"/>

<xsl:output method="xml" indent="yes"/>

<!-- Process the document node. -->
<xsl:template match="/">
  <xsl:apply-templates select="comment() | processing-instruction()"/>
  <xsl:apply-templates select="spirit14:*" mode="root-element"/>
</xsl:template>

<!-- Match any non IPXACT 1.4 element. -->
<xsl:template match="*">
  <xsl:element name="{name()}" namespace="{namespace-uri()}">
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>

<!-- Copy comments, pi's and text. -->
<xsl:template match="comment() | processing-instruction() | text()">
  <xsl:copy>
    <xsl:apply-templates/>
  </xsl:copy>
</xsl:template>

<!-- Match any non IPXACT 1.4 attribute. -->
<xsl:template match="@*">
  <xsl:attribute name="{name()}" namespace="{namespace-uri()}">
    <xsl:value-of select="."/>
  </xsl:attribute>
</xsl:template>

<!-- Match the IPXACT 1.4 root-element. -->
<xsl:template match="spirit14:*" mode="root-element">
  <xsl:element name="spirit:{local-name()}" namespace="{$namespace}">
    <!-- Copy all namespace nodes except for the IPXACT 1.4 namespace node. -->
    <xsl:for-each select="namespace::*">
      <xsl:if test="not(.='http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.4')">
        <xsl:copy/>
      </xsl:if>
    </xsl:for-each>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>

<!-- Change this attribute to point to the SPIRIT 1.5 schema. -->
<xsl:template match="@xsi:schemaLocation">
  <xsl:attribute name="xsi:schemaLocation">
    <xsl:text>http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5 http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5/index.xsd</xsl:text>
  </xsl:attribute>
</xsl:template>

<!-- Match any other IPXACT 1.4 element. -->
<xsl:template match="spirit14:*">
  <xsl:element name="spirit:{local-name()}" namespace="{$namespace}">
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates/>
  </xsl:element>
</xsl:template>

<!-- The attributes need to be handled a little differently, to avoid confusing the 
    processor, the namespaceURI should not be explicitly defined -->
<xsl:template match="@spirit14:*">
  <xsl:attribute name="spirit:{local-name()}" namespace="{$namespace}">
    <xsl:value-of select="."/>
  </xsl:attribute>
</xsl:template>

<xsl:template name="insertComment">
  <xsl:param name="number"/>
  <xsl:param name="message"/>
  <xsl:comment>IP-XACT XSLT Warning#<xsl:value-of select="$number"/>: <xsl:value-of select="$message"/></xsl:comment>
</xsl:template>

<!-- renaming design/interconnections/monitorInterconnection/activeInterface to 
      design/interconnections/monitorInterconnection/monitoredInterface -->

<xsl:template match="/spirit14:design/spirit14:interconnections/spirit14:monitorInterconnection/spirit14:activeInterface">
  <xsl:element name="spirit:monitoredActiveInterface" namespace="{$namespace}">
    <xsl:apply-templates select="@*"/>
    <xsl:value-of select="."/>
  </xsl:element>
</xsl:template>

<!-- renaming design/hierConnections/hierConnection/activeInterface to 
      design/hierConnections/hierConnection/interface -->

<xsl:template match="/spirit14:design/spirit14:hierConnections/spirit14:hierConnection/spirit14:activeInterface">
  <xsl:element name="spirit:interface" namespace="{$namespace}">
    <xsl:apply-templates select="@*"/>
    <xsl:value-of select="."/>
  </xsl:element>
</xsl:template>

<!-- moving field/values into a field/enumeratedValues/enumeratedValue element 
     If register/volatile is true, putting volatile=true and testable=false in the field -->
<xsl:template match="spirit14:field">
  <xsl:element name="spirit:field" namespace="{$namespace}">
    <xsl:apply-templates select="spirit14:name|spirit14:displayName|spirit14:description|spirit14:bitOffset|spirit14:bitWidth"/>
    <xsl:if test="../spirit14:volatile='true'">
      <xsl:element name="spirit:volatile" namespace="{$namespace}">
        <xsl:text>true</xsl:text>
      </xsl:element>
    </xsl:if>
    <xsl:apply-templates select="spirit14:access"/>
    <xsl:if test="spirit14:values">
      <xsl:element name ="spirit:enumeratedValues" namespace="{$namespace}">
        <xsl:for-each select="spirit14:values">
          <xsl:element name="spirit:enumeratedValue" namespace="{$namespace}">
            <xsl:apply-templates select="spirit14:name"/>
            <xsl:apply-templates select="spirit14:description"/>
            <xsl:apply-templates select="spirit14:value"/>
          </xsl:element>
        </xsl:for-each>
      </xsl:element>
    </xsl:if>
    <xsl:if test="../spirit14:volatile='true'">
      <xsl:element name="spirit:testable" namespace="{$namespace}">
        <xsl:text>false</xsl:text>
      </xsl:element>
    </xsl:if>
    <xsl:apply-templates select="spirit14:parameters|spirit14:vendorExtensions"/>
  </xsl:element>
</xsl:template>

<!-- removing volatile=true inside a register since that value was moved into fields -->
<xsl:template match="spirit14:register[spirit14:field]/spirit14:volatile[.='true']"/>

<!-- putting all remapPort elements inside a remapPorts container -->
<xsl:template match="spirit14:remapStates/spirit14:remapState">
  <xsl:element name="spirit:remapState" namespace="{$namespace}">
    <xsl:apply-templates select="spirit14:name|spirit14:displayName|spirit14:description"/>
    <xsl:element name="spirit:remapPorts" namespace="{$namespace}">
      <xsl:apply-templates select="spirit14:remapPort"/>
    </xsl:element>
  </xsl:element>
</xsl:template>

<!-- moving spirit:access from port/transactionl to port -->
<xsl:template match="spirit14:port[spirit14:transactional/spirit14:access]">
  <xsl:element name="spirit:port" namespace="{$namespace}">
    <xsl:apply-templates select="spirit14:name|spirit14:displayName|spirit14:description"/>
    <xsl:element name="spirit:transactional" namespace="{$namespace}">
      <xsl:apply-templates select="spirit14:transactional/spirit14:transTypeDef|spirit14:transactional/spirit14:service|spirit14:transactional/spirit14:connection"/>
    </xsl:element>
    <xsl:apply-templates select="spirit14:transactional/spirit14:access"/>
    <xsl:apply-templates select="spirit14:vendorExtensions"/>
  </xsl:element>
</xsl:template>


<!-- component/model/views/view/fileSetRef/localName <= component/model/views/view/fileSetRef -->
<xsl:template match="/spirit14:component/spirit14:model/spirit14:views/spirit14:view/spirit14:fileSetRef">
  <xsl:element name="spirit:fileSetRef" namespace="{$namespace}">
    <xsl:element name="spirit:localName" namespace="{$namespace}">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:element>
</xsl:template>

<!-- component/busInterfaces/busInterface/slave/fileSetRefGroup/fileSetRef/localName <= 
     component/busInterfaces/busInterface/slave/fileSetRefGroup/fileSetRef -->
<xsl:template match="/spirit14:component/spirit14:busInterfaces/spirit14:busInterface/spirit14:slave/spirit14:fileSetRefGroup/spirit14:fileSetRef">
  <xsl:element name="spirit:fileSetRef" namespace="{$namespace}">
    <xsl:element name="spirit:localName" namespace="{$namespace}">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:element>
</xsl:template>

<!-- component/addressSpaces/addressSpace/executableImage/fileSetRefGroup/fileSetRef/localName <= 
     component/addressSpaces/addressSpace/executableImage/fileSetRefGroup/fileSetRef -->
<xsl:template match="/spirit14:component/spirit14:addressSpaces/spirit14:addressSpace/spirit14:executableImage/spirit14:fileSetRefGroup/spirit14:fileSetRef">
  <xsl:element name="spirit:fileSetRef" namespace="{$namespace}">
    <xsl:element name="spirit:localName" namespace="{$namespace}">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:element>
</xsl:template>

<!-- abstractor/model/views/view/fileSetRef/localName <= abstractor/model/views/view/fileSetRef -->
<xsl:template match="/spirit14:abstractor/spirit14:model/spirit14:views/spirit14:view/spirit14:fileSetRef">
  <xsl:element name="spirit:fileSetRef" namespace="{$namespace}">
    <xsl:element name="spirit:localName" namespace="{$namespace}">
      <xsl:value-of select="."/>
    </xsl:element>
  </xsl:element>
</xsl:template>

<!-- removing spirit14:modeConstraints in spirit14:abstractionDefinition if empty -->

<xsl:template match="spirit14:modeConstraints[not(spirit14:timingConstraint) and not(spirit14:driveConstraint) and not(spirit14:loadConstraint)]">
	<xsl:call-template name="insertComment">
		<xsl:with-param name="number">1</xsl:with-param>
		<xsl:with-param name="message">Removing empty modeConstraints element</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- removing spirit14:mirroredModeConstraints in spirit14:abstractionDefinition if empty -->

<xsl:template match="spirit14:mirroredModeConstraints[not(spirit14:timingConstraint) and not(spirit14:driveConstraint) and not(spirit14:loadConstraint)]">
	<xsl:call-template name="insertComment">
		<xsl:with-param name="number">2</xsl:with-param>
		<xsl:with-param name="message">Removing empty mirroredModeConstraints element</xsl:with-param>
	</xsl:call-template>
</xsl:template>

<!-- removing spirit:phase/@spirit:scope -->

<xsl:template match="spirit14:phase/@spirit14:scope"/>

</xsl:stylesheet>
