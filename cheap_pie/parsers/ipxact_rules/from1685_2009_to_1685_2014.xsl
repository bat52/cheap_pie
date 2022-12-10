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
// Description :  from1685_2009_to_1685_2014.xsl
// XSL transform to go from the 1685-2009 version to the 1685-2014 version of the Schema
// Author: The Accellera System Initiative IP-XACT Schema Working Group
// Date: July 5, 2012
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:spirit="http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009" xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/1685-2014" version="1.0" xmlns:xalan="http://xml.apache.org/xalan" xmlns:exslt="http://exslt.org/common" xmlns:msxsl="urn:schemas-microsoft-com:xslt"  xmlns:kactus2="http://funbase.cs.tut.fi/" exclude-result-prefixes="xalan exslt msxsl spirit">
	<xsl:import href="convert_expressions-other.xsl"/>
	<xsl:import href="convert_expressions-exslt.xsl"/>
	<xsl:import href="convert_expressions-msxsl.xsl"/>
	<xsl:import href="convert_expressions-xalan.xsl"/>
	
	<xsl:param name="catalog"/>
	<xsl:param name="createDesignInstantiation" select="false()"/>
	<xsl:param name="verbose" select="true()"/>
	<xsl:param name="namespace" select="'http://www.accellera.org/XMLSchema/IPXACT/1685-2014'"/>
	<xsl:param name="prefix" select="true()"/>
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
		</xsl:copy>
		<xsl:text>
</xsl:text>
	</xsl:template>
	<xsl:template name="insertComment">
		<xsl:param name="number"/>
		<xsl:param name="message"/>
		<xsl:if test="$verbose">
			<xsl:message>IP-XACT 1685-2014 XSLT Warning#<xsl:value-of select="$number"/>: <xsl:value-of select="$message"/>
			</xsl:message>
		</xsl:if>
		<xsl:comment> IP-XACT 1685-2014 XSLT Warning#<xsl:value-of select="$number"/>: <xsl:value-of select="$message"/>
		</xsl:comment>
	</xsl:template>
	<xsl:template match="@*">
		<xsl:attribute name="{name()}" namespace="{namespace-uri()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template match="/spirit:*">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:for-each select="namespace::*">
				<xsl:if test="not(.='http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009')">
					<xsl:copy/>
				</xsl:if>
			</xsl:for-each>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@xsi:schemaLocation">
		<xsl:attribute name="xsi:schemaLocation"><xsl:text>http://www.accellera.org/XMLSchema/IPXACT/1685-2014 http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd</xsl:text></xsl:attribute>
	</xsl:template>
	<xsl:template match="spirit:*">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	<!-- The attributes are no longer qualified, so the namespace can be removed. -->
	<xsl:template match="@spirit:*">
		<xsl:attribute name="{local-name()}"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<!-- convert executableImage/id to executableImage/imageId-->
	<xsl:template match="spirit:executableImage/@spirit:id">
		<xsl:attribute name="imageId"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<!-- convert cellSpecification -->
	<xsl:template match="spirit:cellSpecification">
		<ipxact:cellSpecification>
			<xsl:apply-templates select="spirit:cellFunction/@spirit:cellStrength"/>
			<xsl:apply-templates select="spirit:cellClass/@spirit:cellStrength"/>
			<xsl:choose>
				<xsl:when test="spirit:cellFunction">
					<ipxact:cellFunction>
						<xsl:value-of select="spirit:cellFunction"/>
					</ipxact:cellFunction>
				</xsl:when>
				<xsl:otherwise>
					<ipxact:cellClass>
						<xsl:value-of select="spirit:cellClass"/>
					</ipxact:cellClass>
				</xsl:otherwise>
			</xsl:choose>
		</ipxact:cellSpecification>
	</xsl:template>
	<!-- bus-interface values -->
	<xsl:template match="spirit:abstractorInterface/spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:left 
  | spirit:abstractorInterface/spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:right 
  | spirit:abstractorInterface/spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:left 
  | spirit:abstractorInterface/spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:right">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:abstractorInterface">
		<ipxact:abstractorInterface>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:portMaps) and not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:left" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:right" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:left" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:right" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:abstractorInterface>
	</xsl:template>
	<xsl:template match="spirit:interconnectionConfiguration/spirit:abstractors">
	  <ipxact:abstractorInstances>
	    <xsl:apply-templates select="@*"/>
	    <xsl:apply-templates/>
	  </ipxact:abstractorInstances>
	</xsl:template>
	<xsl:template match="spirit:interconnectionConfiguration/spirit:abstractors/spirit:abstractor">
	  <ipxact:abstractorInstance>
	    <xsl:apply-templates select="@*"/>
	    <xsl:apply-templates/>
	  </ipxact:abstractorInstance>
	</xsl:template>
	<!-- field values -->
	<xsl:template match="spirit:field/spirit:bitWidth 
  | spirit:field/spirit:writeValueConstraintType/spirit:minimum
  | spirit:field/spirit:writeValueConstraintType/spirit:maximum">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<!-- field offset, eventually followed by a reset extracted from the register level -->
	<xsl:template match="spirit:bitOffset">
		<xsl:variable name="bitWidth">
		  <xsl:apply-templates select="../spirit:bitWidth" mode="parse-expression"/>
		</xsl:variable>
		<ipxact:bitOffset>
			<xsl:value-of select="."/>
		</ipxact:bitOffset>
		<xsl:if test="../../spirit:reset">
			<ipxact:resets>
				<ipxact:reset>
					<xsl:variable name="value">
						<xsl:apply-templates select="../../spirit:reset/spirit:value" mode="parse-expression"/>
					</xsl:variable>
					<ipxact:value>
						<xsl:call-template name="field-value">
							<xsl:with-param name="value" select="$value"/>
							<xsl:with-param name="bitOffset" select="."/>
							<xsl:with-param name="bitWidth" select="$bitWidth"/>
						</xsl:call-template>
					</ipxact:value>
					<xsl:if test="../../spirit:reset/spirit:mask">
						<xsl:variable name="mask">
							<xsl:apply-templates select="../../spirit:reset/spirit:mask" mode="parse-expression"/>
						</xsl:variable>
						<ipxact:mask>
							<xsl:call-template name="field-value">
								<xsl:with-param name="value" select="$mask"/>
								<xsl:with-param name="bitOffset" select="."/>
								<xsl:with-param name="bitWidth" select="$bitWidth"/>
							</xsl:call-template>
						</ipxact:mask>
					</xsl:if>
				</ipxact:reset>
			</ipxact:resets>
		</xsl:if>
	</xsl:template>
	<xsl:template match="spirit:field">
		<ipxact:field>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:bitWidth" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:writeValueConstraintType/spirit:minimum" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:writeValueConstraintType/spirit:maximum" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:field>
	</xsl:template>
	<!-- register values -->
	<xsl:template match="spirit:register/spirit:size
  | spirit:register/spirit:reset/spirit:value
  | spirit:register/spirit:reset/spirit:mask">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:register">
		<ipxact:register>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="spirit:name"/>
			<xsl:apply-templates select="spirit:displayName"/>
			<xsl:apply-templates select="spirit:description"/>
			<xsl:variable name="path">
				<xsl:for-each select="ancestor-or-self::*[spirit:name and not(self::spirit:component)]">
					<xsl:value-of select="spirit:name"/>
				</xsl:for-each>
			</xsl:variable>
			<xsl:if test="/spirit:component/spirit:whiteboxElements/spirit:whiteboxElement[translate(spirit:registerRef, '/', '')=$path]">
				<xsl:variable name="whiteboxName" select="/spirit:component/spirit:whiteboxElements/spirit:whiteboxElement[translate(spirit:registerRef, '/', '')=$path]/spirit:name"/>
				<xsl:choose>
					<xsl:when test="/spirit:component/spirit:model/spirit:views/spirit:view/spirit:whiteboxElementRefs/spirit:whiteboxElementRef[@spirit:name=$whiteboxName]">
						<ipxact:accessHandles>
							<xsl:for-each select="/spirit:component/spirit:model/spirit:views/spirit:view/spirit:whiteboxElementRefs/spirit:whiteboxElementRef[@spirit:name=$whiteboxName]">
								<ipxact:accessHandle>
									<ipxact:viewRef>
										<xsl:value-of select="../../spirit:name"/>
									</ipxact:viewRef>
									<ipxact:slices>
										<xsl:for-each select="spirit:whiteboxPath">
											<ipxact:slice>
												<xsl:apply-templates select="."/>
											</ipxact:slice>
										</xsl:for-each>
									</ipxact:slices>
								</ipxact:accessHandle>
							</xsl:for-each>
						</ipxact:accessHandles>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="insertComment">
							<xsl:with-param name="number">1</xsl:with-param>
							<xsl:with-param name="message">Unable to find whiteboxElementRef for whiteboxElement with name '<xsl:value-of select="$whiteboxName"/>'.</xsl:with-param>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
			<xsl:apply-templates select="*[not(self::spirit:name) and not(self::spirit:displayName) and not(self::spirit:description) and not(self::spirit:parameters) and not(self::spirit:vendorExtensions) and not (self::spirit:alternateRegisters) ]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:size" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:reset/spirit:value" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:reset/spirit:mask" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>

			<xsl:if test="( (sum(spirit:field/spirit:bitWidth) &lt; spirit:size) or spirit:size/@spirit:dependency or spirit:field/spirit:bitWidth/@spirit:dependency) and spirit:reset and count(spirit:field) &gt; 0">
				<xsl:message>&#xa;[WARNING] spirit:size of register : [<xsl:value-of select="spirit:name"/>]</xsl:message>
				<xsl:message>          is not fully covered by fields or its size or one of the field size is dependent.</xsl:message>
				<xsl:message>          you may consider to create bitfields, before using this xsl transform</xsl:message>
				<xsl:message>          to ensure the reset value will be fully propagated from the register level to the field level</xsl:message>
			</xsl:if>

			<xsl:if test="not(spirit:field)">
				<xsl:comment>field was infered from the register definition since one field must exists within the new schema</xsl:comment>
				<ipxact:field>
					<ipxact:name>
						<xsl:value-of select="./spirit:name"/>
					</ipxact:name>
					<ipxact:bitOffset>0</ipxact:bitOffset>
					<xsl:if test="spirit:reset">
						<ipxact:resets>
							<ipxact:reset>
								<ipxact:value>
									<xsl:choose>
										<xsl:when test="spirit:reset/spirit:value/@spirit:dependency">
											<xsl:call-template name="parse-expression">
												<xsl:with-param name="value" select="spirit:reset/spirit:value/@spirit:dependency"/>
											</xsl:call-template>
										</xsl:when>
										<xsl:otherwise>
											<xsl:call-template name="parse-scale">
												<xsl:with-param name="value" select="normalize-space(spirit:reset/spirit:value)"/>
											</xsl:call-template>
										</xsl:otherwise>
									</xsl:choose>
								</ipxact:value>
								<xsl:if test="spirit:reset/spirit:mask">
									<ipxact:mask>
										<xsl:choose>
											<xsl:when test="spirit:reset/spirit:mask/@spirit:dependency">
												<xsl:call-template name="parse-expression">
													<xsl:with-param name="value" select="spirit:reset/spirit:mask/@spirit:dependency"/>
												</xsl:call-template>
											</xsl:when>
											<xsl:otherwise>
												<xsl:call-template name="parse-scale">
													<xsl:with-param name="value" select="normalize-space(spirit:reset/spirit:mask)"/>
												</xsl:call-template>
											</xsl:otherwise>
										</xsl:choose>
									</ipxact:mask>
								</xsl:if>
							</ipxact:reset>
						</ipxact:resets>
					</xsl:if>
					<ipxact:bitWidth>
						<xsl:choose>
							<xsl:when test="spirit:size/@spirit:dependency">
								<xsl:call-template name="parse-expression">
									<xsl:with-param name="value" select="spirit:size/@spirit:dependency"/>
								</xsl:call-template>
							</xsl:when>
							<xsl:otherwise>
								<xsl:call-template name="parse-scale">
									<xsl:with-param name="value" select="normalize-space(spirit:size)"/>
								</xsl:call-template>
							</xsl:otherwise>
						</xsl:choose>
					</ipxact:bitWidth>
				</ipxact:field>
			</xsl:if>
			<xsl:apply-templates select="spirit:alternateRegisters"/>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:register>
	</xsl:template>
	<!-- alternateRegister values -->
	<xsl:template match="spirit:alternateRegister/spirit:reset/spirit:value
  | spirit:alternateRegister/spirit:reset/spirit:mask">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:alternateRegister">
		<ipxact:alternateRegister>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<!-- auto infer a field if the alternate register did not had one-->
			<xsl:if test="not(spirit:field)">
				<xsl:comment>field was infered from the register definition since one field must exists within the new schema</xsl:comment>
				<ipxact:field>
					<ipxact:name>
						<xsl:value-of select="./spirit:name"/>
					</ipxact:name>
					<ipxact:bitOffset>0</ipxact:bitOffset>
					<xsl:if test="spirit:reset">
						<ipxact:resets>
							<ipxact:reset>
								<ipxact:value>
									<xsl:choose>
										<xsl:when test="spirit:reset/spirit:value/@spirit:dependency">
											<xsl:call-template name="parse-expression">
												<xsl:with-param name="value" select="spirit:reset/spirit:value/@spirit:dependency"/>
											</xsl:call-template>
										</xsl:when>
										<xsl:otherwise>
											<xsl:call-template name="parse-scale">
												<xsl:with-param name="value" select="normalize-space(spirit:reset/spirit:value)"/>
											</xsl:call-template>
										</xsl:otherwise>
									</xsl:choose>
								</ipxact:value>
								<xsl:if test="spirit:reset/spirit:mask">
									<ipxact:mask>
										<xsl:choose>
											<xsl:when test="spirit:reset/spirit:mask/@spirit:dependency">
												<xsl:call-template name="parse-expression">
													<xsl:with-param name="value" select="spirit:reset/spirit:mask/@spirit:dependency"/>
												</xsl:call-template>
											</xsl:when>
											<xsl:otherwise>
												<xsl:call-template name="parse-scale">
													<xsl:with-param name="value" select="normalize-space(spirit:reset/spirit:mask)"/>
												</xsl:call-template>
											</xsl:otherwise>
										</xsl:choose>
									</ipxact:mask>
								</xsl:if>
							</ipxact:reset>
						</ipxact:resets>
					</xsl:if>
					<ipxact:bitWidth>
						<xsl:choose>
							<xsl:when test="../../spirit:size/@spirit:dependency">
								<xsl:call-template name="parse-expression">
									<xsl:with-param name="value" select="../../spirit:size/@spirit:dependency"/>
								</xsl:call-template>
							</xsl:when>
							<xsl:otherwise>
								<xsl:call-template name="parse-scale">
									<xsl:with-param name="value" select="normalize-space(../../spirit:size)"/>
								</xsl:call-template>
							</xsl:otherwise>
						</xsl:choose>
					</ipxact:bitWidth>
				</ipxact:field>
			</xsl:if>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:reset/spirit:value" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:reset/spirit:mask" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:alternateRegister>
	</xsl:template>
	<!-- RegisterFile values -->
	<xsl:template match="spirit:registerFile/spirit:range">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:registerFile">
		<ipxact:registerFile>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:range" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:registerFile>
	</xsl:template>
	<!-- AddressBlock values -->
	<xsl:template match="spirit:addressBlock/spirit:baseAddress
  | spirit:addressBlock/spirit:range
  | spirit:addressBlock/spirit:width">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:addressBlock">
		<ipxact:addressBlock>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions) and not(self::spirit:register) and not(self::spirit:registerFile)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:baseAddress" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:range" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:width" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:register"/>
			<xsl:apply-templates select="spirit:registerFile"/>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:addressBlock>
	</xsl:template>
	<!-- Bank values -->
	<xsl:template match="spirit:bank/spirit:baseAddress">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:bank">
		<ipxact:bank>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:baseAddress" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:bank>
	</xsl:template>
	<!-- Bank values -->
	<xsl:template match="spirit:subspaceMap/spirit:baseAddress">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:subspaceMap">
		<ipxact:subspaceMap>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:baseAddress" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:subspaceMap>
	</xsl:template>
	<!-- Executable Image values -->
	<xsl:template match="spirit:executableImage/spirit:languageTools/spirit:fileBuilder/spirit:command
  | spirit:executableImage/spirit:languageTools/spirit:fileBuilder/spirit:flags
  | spirit:executableImage/spirit:languageTools/spirit:fileBuilder/spirit:replaceDefaultFlags
  | spirit:executableImage/spirit:languageTools/spirit:linker
  | spirit:executableImage/spirit:languageTools/spirit:linkerFlags
  | spirit:executableImage/spirit:languageTools/spirit:linkerCommandFile/spirit:name
  | spirit:executableImage/spirit:languageTools/spirit:linkerCommandFile/spirit:commandLineSwitch
  | spirit:executableImage/spirit:languageTools/spirit:linkerCommandFile/spirit:enable">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:configurableElementValue">
		<xsl:call-template name="convert-scaled"/>
	</xsl:template>
	<xsl:template match="spirit:executableImage">
		<ipxact:executableImage>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="spirit:name"/>
			<xsl:apply-templates select="spirit:description"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:languageTools/spirit:fileBuilder/spirit:command" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:fileBuilder/spirit:flags" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:fileBuilder/spirit:replaceDefaultFlags" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:linker" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:linkerFlags" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:linkerCommandFile/spirit:name" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:linkerCommandFile/spirit:commandLineSwitch" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:languageTools/spirit:linkerCommandFile/spirit:enable" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:languageTools"/>
			<xsl:apply-templates select="spirit:fileSetRefGroup"/>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:executableImage>
	</xsl:template>
	<!-- Convert tiedValue from attribute to element -->
	<xsl:template match="spirit:adHocConnection">
		<ipxact:adHocConnection>
			<xsl:apply-templates select="spirit:name"/>
			<xsl:apply-templates select="spirit:displayName"/>
			<xsl:apply-templates select="spirit:description"/>
			<xsl:if test="@spirit:tiedValue">
				<ipxact:tiedValue>
					<xsl:call-template name="parse-scale">
						<xsl:with-param name="value" select="normalize-space(@spirit:tiedValue)"/>
					</xsl:call-template>
				</ipxact:tiedValue>
			</xsl:if>
			<ipxact:portReferences>
				<xsl:apply-templates select="spirit:internalPortReference"/>
				<xsl:apply-templates select="spirit:externalPortReference"/>
			</ipxact:portReferences>
		</ipxact:adHocConnection>
	</xsl:template>
	<!-- Convert Scaled -->
	<xsl:template match="spirit:register/spirit:addressOffset
  | spirit:enumeratedValue/spirit:value
  | spirit:registerFile/spirit:addressOffset
  | spirit:wire/spirit:defaultValue">
		<xsl:call-template name="convert-scaled"/>
	</xsl:template>
	<xsl:template match="spirit:model/spirit:ports/spirit:port/spirit:wire">
		<ipxact:wire>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="spirit:direction"/>
			<xsl:apply-templates select="spirit:vector"/>
			<xsl:apply-templates select="spirit:wireTypeDefs"/>
			<xsl:apply-templates select="spirit:driver"/>
			<xsl:apply-templates select="spirit:constraintSets"/>
		</ipxact:wire>
	</xsl:template>
	<!-- Address Space values -->
	<xsl:template match="spirit:addressSpace/spirit:range
  | spirit:addressSpace/spirit:width
  | spirit:addressSpace/spirit:segments/spirit:segment/spirit:addressOffset
  | spirit:addressSpace/spirit:segments/spirit:segment/spirit:range">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:addressSpace">
		<ipxact:addressSpace>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:range" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:width" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:segments/spirit:segment/spirit:addressOffset" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:segments/spirit:segment/spirit:range" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:addressSpace>
	</xsl:template>
	<!-- View values -->
	<xsl:template match="spirit:view/spirit:defaultFileBuilder/spirit:command
  | spirit:view/spirit:defaultFileBuilder/spirit:flags
  | spirit:view/spirit:defaultFileBuilder/spirit:replaceDefaultFlags">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:view">
		<ipxact:view>
			<xsl:for-each select="namespace::*">
				<xsl:if test="not(.='http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009')">
					<xsl:copy/>
				</xsl:if>
			</xsl:for-each>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:defaultFileBuilder/spirit:command" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:defaultFileBuilder/spirit:flags" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:defaultFileBuilder/spirit:replaceDefaultFlags" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:view>
	</xsl:template>
	<!-- Component/Abstractor values -->
	<xsl:template match="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:vector/spirit:left
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:vector/spirit:right
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:defaultValue
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPeriod
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPulseOffset
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPulseValue
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPulseDuration
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:singleShotDriver/spirit:singleShotOffset
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:singleShotDriver/spirit:singleShotValue
  | spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:singleShotDriver/spirit:singleShotDuration
  | spirit:fileSets/spirit:fileSet/spirit:file/spirit:name
  | spirit:fileSets/spirit:fileSet/spirit:file/spirit:define/spirit:value
  | spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:command
  | spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:flags
  | spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:replaceDefaultFlags
  | spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:targetName
  | spirit:fileSets/spirit:fileSet/spirit:defaultFileBuilder/spirit:command
  | spirit:fileSets/spirit:fileSet/spirit:defaultFileBuilder/spirit:flags
  | spirit:fileSets/spirit:fileSet/spirit:defaultFileBuilder/spirit:replaceDefaultFlags
  | spirit:fileSets/spirit:fileSet/spirit:function/spirit:argument/spirit:value
  | spirit:fileSets/spirit:fileSet/spirit:function/spirit:disabled
  | spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPeriod
  | spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPulseOffset
  | spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPulseValue
  | spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPulseDuration">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="/spirit:component | /spirit:abstractor" priority="1">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:for-each select="namespace::*">
				<xsl:if test="not(.='http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009')">
					<xsl:copy/>
				</xsl:if>
			</xsl:for-each>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:model/spirit:modelParameters/spirit:modelParameter" mode="convert-to-parameter"/>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:vector/spirit:left" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:vector/spirit:right" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:defaultValue" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPulseValue" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:singleShotDriver/spirit:singleShotValue" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPeriod" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPulseDuration" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:clockDriver/spirit:clockPulseOffset" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:singleShotDriver/spirit:singleShotOffset" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver/spirit:singleShotDriver/spirit:singleShotDuration" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:file/spirit:name" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:file/spirit:define/spirit:value" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:command" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:flags" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:replaceDefaultFlags" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:file/spirit:buildCommand/spirit:targetName" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:defaultFileBuilder/spirit:command" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:defaultFileBuilder/spirit:flags" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:defaultFileBuilder/spirit:replaceDefaultFlags" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:function/spirit:argument/spirit:value" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:fileSets/spirit:fileSet/spirit:function/spirit:disabled" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPeriod" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPulseDuration" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPulseValue" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:otherClockDrivers/spirit:otherClockDriver/spirit:clockPulseOffset" mode="convert-to-parameter">
					<xsl:with-param name="format">real</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:views/spirit:view/spirit:defaultFileBuilder/spirit:command" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:views/spirit:view/spirit:defaultFileBuilder/spirit:flags" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:model/spirit:views/spirit:view/spirit:defaultFileBuilder/spirit:replaceDefaultFlags" mode="convert-to-parameter">
					<xsl:with-param name="format">bit</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</xsl:element>
	</xsl:template>
	<!-- bus-interface values -->
	<xsl:template match="spirit:busInterface/spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:left 
  | spirit:busInterface/spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:right 
  | spirit:busInterface/spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:left 
  | spirit:busInterface/spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:right
  | spirit:busInterface/spirit:master/spirit:addressSpaceRef/spirit:baseAddress
  | spirit:busInterface/spirit:mirroredSlave/spirit:baseAddresses/spirit:remapAddress
  | spirit:busInterface/spirit:mirroredSlave/spirit:baseAddresses/spirit:range
  | spirit:busInterface/spirit:bitSteering">
		<xsl:call-template name="convert-expression"/>
	</xsl:template>
	<xsl:template match="spirit:bridge">
		<xsl:if test="@spirit:opaque = 'false'">
			<ipxact:transparentBridge masterRef="{@spirit:masterRef}"/>
		</xsl:if>
	</xsl:template>
	<xsl:template match="spirit:busInterface">
		<ipxact:busInterface>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="*[not(self::spirit:portMaps) and not(self::spirit:parameters) and not(self::spirit:vendorExtensions)]"/>
			<xsl:variable name="params">
				<xsl:apply-templates select="spirit:parameters/spirit:parameter"/>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:left" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:logicalPort/spirit:vector/spirit:right" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:left" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:portMaps/spirit:portMap/spirit:physicalPort/spirit:vector/spirit:right" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:master/spirit:addressSpaceRef/spirit:baseAddress" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:mirroredSlave/spirit:baseAddresses/spirit:remapAddress" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:mirroredSlave/spirit:baseAddresses/spirit:range" mode="convert-to-parameter">
					<xsl:with-param name="format">longint</xsl:with-param>
				</xsl:apply-templates>
				<xsl:apply-templates select="spirit:bitSteering" mode="convert-to-parameter">
					<xsl:with-param name="format">string</xsl:with-param>
				</xsl:apply-templates>
			</xsl:variable>
			<xsl:call-template name="write-parameters">
				<xsl:with-param name="params" select="$params"/>
			</xsl:call-template>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:busInterface>
	</xsl:template>
	<xsl:template name="convert-expression">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:apply-templates select="@spirit:minimum"/>
			<xsl:apply-templates select="@spirit:maximum"/>
			<xsl:apply-templates select="@*" mode="convert-non-expression-parameters"/>
			<xsl:choose>
				<xsl:when test="@spirit:dependency">
					<xsl:call-template name="parse-expression">
						<xsl:with-param name="value" select="@spirit:dependency"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="@spirit:id">
					<xsl:value-of select="@spirit:id"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="parse-scale">
						<xsl:with-param name="value" select="normalize-space(.)"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:element>
	</xsl:template>

  <xsl:template match="@spirit:dependency | @spirit:minimum | @spirit:maximum | @spirit:dependency | @spirit:id | @spirit:format | @spirit:resolve | @spirit:choiceRef | @spirit:order | @spirit:configGroups | @spirit:bitStringLength | @spirit:rangeType | @spirit:prompt" mode="convert-non-expression-parameters"/>

  <xsl:template match="@*" mode="convert-non-expression-parameters">
    <xsl:apply-templates select="."/>
  </xsl:template>
  
  <xsl:template name="convert-scaled">
		<xsl:element name="ipxact:{local-name()}" namespace="{$namespace}">
			<xsl:apply-templates select="@*"/>
			<xsl:call-template name="parse-scale">
				<xsl:with-param name="value" select="normalize-space(.)"/>
			</xsl:call-template>
		</xsl:element>
	</xsl:template>

	<xsl:template match="*" mode="parse-expression">
		<xsl:choose>
			<xsl:when test="@spirit:dependency">
				<xsl:call-template name="parse-expression">
					<xsl:with-param name="value" select="@spirit:dependency"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="parse-scale">
					<xsl:with-param name="value" select="normalize-space(.)"/>
					<xsl:with-param name="bit-length" select="@spirit:bitStringLength"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
  </xsl:template>
	  
	<xsl:template match="*[@spirit:id]" mode="convert-to-parameter">
		<xsl:param name="format">string</xsl:param>
		<ipxact:parameter>
			<xsl:if test="@spirit:id">
				<xsl:attribute name="parameterId"><xsl:value-of select="@spirit:id"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@spirit:resolve = 'user'">
				<xsl:attribute name="resolve">user</xsl:attribute>
			</xsl:if>
			<xsl:if test="@spirit:resolve = 'generated'">
				<xsl:attribute name="resolve">generated</xsl:attribute>
			</xsl:if>
			<xsl:if test="not(@spirit:format)">
				<xsl:attribute name="type"><xsl:value-of select="$format"/></xsl:attribute>
			</xsl:if>
			<xsl:apply-templates select="@spirit:format"/>
			<xsl:apply-templates select="@spirit:choiceRef"/>
			<xsl:apply-templates select="@spirit:order"/>
			<xsl:apply-templates select="@spirit:configGroups"/>
			<xsl:apply-templates select="@spirit:prompt"/>
			<xsl:apply-templates select="@spirit:minimum"/>
			<xsl:apply-templates select="@spirit:maximum"/>
			<ipxact:name>
				<xsl:value-of select="@spirit:id"/>
			</ipxact:name>
			<xsl:apply-templates select="@spirit:bitStringLength"/>
			<ipxact:value>
				<xsl:choose>
					<xsl:when test="@spirit:dependency">
						<xsl:call-template name="parse-expression">
							<xsl:with-param name="value" select="@spirit:dependency"/>
						</xsl:call-template>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="parse-scale">
							<xsl:with-param name="value" select="normalize-space(.)"/>
							<xsl:with-param name="bit-length" select="@spirit:bitStringLength"/>
						</xsl:call-template>
					</xsl:otherwise>
				</xsl:choose>
			</ipxact:value>
		</ipxact:parameter>
	</xsl:template>
	<xsl:template match="@spirit:format">
		<xsl:attribute name="type"><xsl:choose><xsl:when test=".='bool'">bit</xsl:when><xsl:when test=".='long'">longint</xsl:when><xsl:when test=".='bitString'">bit</xsl:when><xsl:when test=".='float'">real</xsl:when><xsl:otherwise><xsl:value-of select="."/></xsl:otherwise></xsl:choose></xsl:attribute>
	</xsl:template>

	<xsl:template name="field-value">
		<xsl:param name="bitWidth"/>
		<xsl:param name="bitOffset"/>
		<xsl:param name="value"/>
		<xsl:value-of select="concat('(', $value, ') / $pow(2,', $bitOffset, ') % $pow(2,', $bitWidth, ')')"/>
	</xsl:template>

	<xsl:template match="spirit:modelParameter">
		<ipxact:moduleParameter>
			<xsl:apply-templates select="spirit:value/@spirit:format"/>
			<xsl:apply-templates select="spirit:value/@spirit:minimum"/>
			<xsl:apply-templates select="spirit:value/@spirit:maximum"/>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="spirit:name"/>
			<xsl:apply-templates select="spirit:displayName"/>
			<xsl:apply-templates select="spirit:description"/>
			<xsl:apply-templates select="spirit:value/@spirit:bitStringLength"/>
		  <xsl:choose>
		    <xsl:when test="spirit:value/@spirit:id"><ipxact:value><xsl:value-of select="spirit:value/@spirit:id"/></ipxact:value></xsl:when>
				<xsl:otherwise><xsl:apply-templates select="spirit:value"/></xsl:otherwise>
	    </xsl:choose>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:moduleParameter>
	</xsl:template>
	<xsl:template match="spirit:modelParameter" mode="convert-to-parameter">
		<xsl:if test="spirit:value/@spirit:id">
			<ipxact:parameter>
				<xsl:attribute name="parameterId"><xsl:value-of select="spirit:value/@spirit:id"/></xsl:attribute>
  			<xsl:if test="spirit:value/@spirit:resolve = 'user'">
  				<xsl:attribute name="resolve">user</xsl:attribute>
  			</xsl:if>
  			<xsl:if test="spirit:value/@spirit:resolve = 'generated'">
  				<xsl:attribute name="resolve">generated</xsl:attribute>
  			</xsl:if>
  			<xsl:apply-templates select="spirit:value/@spirit:format"/>
  			<xsl:apply-templates select="spirit:value/@spirit:choiceRef"/>
  			<xsl:apply-templates select="spirit:value/@spirit:order"/>
  			<xsl:apply-templates select="spirit:value/@spirit:configGroups"/>
  			<xsl:apply-templates select="spirit:value/@spirit:prompt"/>
  			<xsl:apply-templates select="spirit:value/@spirit:minimum"/>
  			<xsl:apply-templates select="spirit:value/@spirit:maximum"/>
  			<xsl:apply-templates select="@*[not(namespace-uri() = 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009')]"/>
  			<xsl:apply-templates select="spirit:name"/>
  			<xsl:apply-templates select="spirit:displayName"/>
  			<xsl:apply-templates select="spirit:description"/>
  			<xsl:apply-templates select="spirit:value/@spirit:bitStringLength"/>
  			<xsl:apply-templates select="spirit:value"/>
  			<xsl:apply-templates select="spirit:vendorExtensions"/>
  		</ipxact:parameter>
  	</xsl:if>
	</xsl:template>
	<xsl:template match="spirit:parameter">
		<ipxact:parameter>
			<xsl:if test="spirit:value/@spirit:id">
				<xsl:attribute name="parameterId"><xsl:value-of select="spirit:value/@spirit:id"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="spirit:value/@spirit:resolve = 'user'">
				<xsl:attribute name="resolve">user</xsl:attribute>
			</xsl:if>
			<xsl:if test="spirit:value/@spirit:resolve = 'generated'">
				<xsl:attribute name="resolve">generated</xsl:attribute>
			</xsl:if>
			<xsl:apply-templates select="spirit:value/@spirit:format"/>
			<xsl:apply-templates select="spirit:value/@spirit:choiceRef"/>
			<xsl:apply-templates select="spirit:value/@spirit:order"/>
			<xsl:apply-templates select="spirit:value/@spirit:configGroups"/>
			<xsl:apply-templates select="spirit:value/@spirit:prompt"/>
			<xsl:apply-templates select="spirit:value/@spirit:minimum"/>
			<xsl:apply-templates select="spirit:value/@spirit:maximum"/>
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="spirit:name"/>
			<xsl:apply-templates select="spirit:displayName"/>
			<xsl:apply-templates select="spirit:description"/>
			<xsl:apply-templates select="spirit:value/@spirit:bitStringLength"/>
			<xsl:apply-templates select="spirit:value"/>
			<xsl:apply-templates select="spirit:vendorExtensions"/>
		</ipxact:parameter>
	</xsl:template>
	
	<xsl:template match="@spirit:bitStringLength">
		<ipxact:vectors>
			<ipxact:vector>
				<ipxact:left>0</ipxact:left>
				<ipxact:right>
					<xsl:value-of select="."/>
				</ipxact:right>
			</ipxact:vector>
		</ipxact:vectors>
	</xsl:template>
	
	<xsl:template match="spirit:parameter/spirit:value | spirit:modelParameter/spirit:value">
    <xsl:if test="not(text()) and not(@spirit:dependency)">
      <xsl:message>WARNING: Generating value for parameter <xsl:value-of select="../spirit:name"/>.</xsl:message>
      <xsl:comment>WARNING: Generated value.</xsl:comment>
    </xsl:if>
		<ipxact:value>
		  <xsl:apply-templates select="@*[not(namespace-uri() = 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1685-2009')]"/>
			<xsl:choose>
				<xsl:when test="@spirit:dependency">
					<xsl:call-template name="parse-expression">
						<xsl:with-param name="value" select="@spirit:dependency"/>
					</xsl:call-template>
				</xsl:when>
  	    <xsl:when test="not(text())">
		      <xsl:choose>
		        <xsl:when test="@spirit:format='bitString'">0</xsl:when>
		        <xsl:when test="@spirit:format='bool'">false</xsl:when>
		        <xsl:when test="@spirit:format='float'">0</xsl:when>
		        <xsl:when test="@spirit:format='long'">0</xsl:when>
		        <xsl:when test="@spirit:format='string'">""</xsl:when>
		        <xsl:otherwise>""</xsl:otherwise>
		      </xsl:choose>
			  </xsl:when>
			  <xsl:otherwise>
					<xsl:call-template name="parse-scale">
						<xsl:with-param name="value" select="normalize-space(.)"/>
						<xsl:with-param name="bit-length" select="@spirit:bitStringLength"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</ipxact:value>
	</xsl:template>

	<!-- component: convert model/views/view/modelName to model/views/view/instantiationType -->
	<xsl:template match="spirit:model/spirit:views/spirit:view/spirit:modelName">
		<xsl:variable name="text" select="translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
		<xsl:choose>
		  <xsl:when test="$text = 'vhdl'">
		    <xsl:choose>
    			<xsl:when test="contains(.,'(') and contains(., ')')">
    				<ipxact:moduleName>
    					<xsl:value-of select="substring-before(., '(')"/>
    				</ipxact:moduleName>
    				<ipxact:architectureName>
    					<xsl:value-of select="substring-before(substring-after(.,'('), ')')"/>
    				</ipxact:architectureName>
    			</xsl:when>
    			<xsl:otherwise>
    				<ipxact:configurationName>
    					<xsl:value-of select="."/>
    				</ipxact:configurationName>
    			</xsl:otherwise>
  			</xsl:choose>
		  </xsl:when>
  		<xsl:otherwise>
  			<ipxact:moduleName>
  				<xsl:value-of select="."/>
  			</ipxact:moduleName>
  		</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<!-- component/abstractor: 
          - convert model/modelParameters to model/views/view/modelParameters
          - convert view/hierarchyRef into hierarchicalView/hierarchyRef -->
	<xsl:template match="spirit:model/spirit:views/spirit:view">
		<xsl:if test="not(spirit:hierarchyRef)">
			<ipxact:componentInstantiation>
				<xsl:apply-templates select="spirit:name"/>
				<xsl:apply-templates select="spirit:displayName"/>
				<xsl:apply-templates select="spirit:description"/>
				<xsl:apply-templates select="spirit:language"/>
				<xsl:apply-templates select="spirit:modelName"/>
				<xsl:apply-templates select="../../spirit:modelParameters"/>
				<!--
  			<xsl:if test="count(spirit:language) > 0">
					<xsl:apply-templates select="../../spirit:modelParameters"/>
				</xsl:if>
-->
				<xsl:apply-templates select="spirit:defaultFileBuilder"/>
				<xsl:apply-templates select="spirit:fileSetRef"/>
				<xsl:apply-templates select="spirit:constraintSetRef"/>
				<xsl:apply-templates select="spirit:whiteboxElementRefs"/>
				<xsl:apply-templates select="spirit:parameters"/>
  			<xsl:apply-templates select="spirit:vendorExtensions"/>
			</ipxact:componentInstantiation>
		</xsl:if>
		<xsl:if test="spirit:hierarchyRef">
			<xsl:choose>
				<xsl:when test="$catalog">
					<xsl:variable name="vendor" select="spirit:hierarchyRef/@spirit:vendor"/>
					<xsl:variable name="library" select="spirit:hierarchyRef/@spirit:library"/>
					<xsl:variable name="name" select="spirit:hierarchyRef/@spirit:name"/>
					<xsl:variable name="version" select="spirit:hierarchyRef/@spirit:version"/>
					<xsl:choose>
						<xsl:when test="document($catalog)/ipxact:catalog/ipxact:designConfigurations/ipxact:ipxactFile/ipxact:vlnv[@vendor=$vendor and @library=$library and @name=$name and @version=$version]">
							<ipxact:designConfigurationInstantiation>
								<xsl:apply-templates select="spirit:name"/>
								<xsl:apply-templates select="spirit:displayName"/>
								<xsl:apply-templates select="spirit:description"/>
								<ipxact:designConfigurationRef>
									<xsl:apply-templates select="spirit:hierarchyRef/@* | spirit:hierarchyRef/node()"/>
								</ipxact:designConfigurationRef>
								<xsl:apply-templates select="spirit:vendorExtensions"/>
							</ipxact:designConfigurationInstantiation>
							<ipxact:designInstantiation>
								<ipxact:name>
									<xsl:value-of select="spirit:name"/>_design</ipxact:name>
								<xsl:apply-templates select="document($catalog)/ipxact:catalog/ipxact:designConfigurations/ipxact:ipxactFile[ipxact:vlnv/@vendor=$vendor and ipxact:vlnv/@library=$library and ipxact:vlnv/@name=$name and ipxact:vlnv/@version=$version]/ipxact:name" mode="move-design-ref"/>
							</ipxact:designInstantiation>
						</xsl:when>
						<xsl:when test="document($catalog)/ipxact:catalog/ipxact:designs/ipxact:ipxactFile/ipxact:vlnv[@vendor=$vendor and @library=$library and @name=$name and @version=$version]">
							<ipxact:designInstantiation>
								<xsl:apply-templates select="spirit:name"/>
								<xsl:apply-templates select="spirit:displayName"/>
								<xsl:apply-templates select="spirit:description"/>
								<ipxact:designRef>
									<xsl:apply-templates select="spirit:hierarchyRef/@* | spirit:hierarchyRef/node()"/>
								</ipxact:designRef>
								<xsl:apply-templates select="spirit:vendorExtensions"/>
							</ipxact:designInstantiation>
						</xsl:when>
						<xsl:otherwise>
							<xsl:message>WARNING: Unable to resolve <xsl:value-of select="$vendor"/> - <xsl:value-of select="$library"/> - <xsl:value-of select="$name"/> - <xsl:value-of select="$version"/> assuming design.</xsl:message>
							<xsl:call-template name="create-default-instantiation"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<xsl:call-template name="create-default-instantiation"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
	<xsl:template name="create-default-instantiation">
		<xsl:choose>
			<xsl:when test="$createDesignInstantiation">
				<ipxact:designInstantiation>
					<xsl:apply-templates select="spirit:name"/>
					<xsl:apply-templates select="spirit:displayName"/>
					<xsl:apply-templates select="spirit:description"/>
					<ipxact:designRef>
						<xsl:apply-templates select="spirit:hierarchyRef/@* | spirit:hierarchyRef/node()"/>
					</ipxact:designRef>
					<xsl:apply-templates select="spirit:vendorExtensions"/>
				</ipxact:designInstantiation>
			</xsl:when>
			<xsl:otherwise>
				<ipxact:designConfigurationInstantiation>
					<xsl:apply-templates select="spirit:name"/>
					<xsl:apply-templates select="spirit:displayName"/>
					<xsl:apply-templates select="spirit:description"/>
					<ipxact:designConfigurationRef>
						<xsl:apply-templates select="spirit:hierarchyRef/@* | spirit:hierarchyRef/node()"/>
					</ipxact:designConfigurationRef>
					<xsl:apply-templates select="spirit:vendorExtensions"/>
				</ipxact:designConfigurationInstantiation>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="/ipxact:catalog/ipxact:designConfigurations/ipxact:ipxactFile/ipxact:name" mode="move-design-ref">
		<xsl:apply-templates select="document(.)/spirit:designConfiguration/spirit:designRef"/>
	</xsl:template>
	<xsl:template match="spirit:model/spirit:views" mode="create-view-groups">
	  <ipxact:views>
	    <xsl:for-each select="spirit:view">
    		<ipxact:view>
    			<xsl:apply-templates select="spirit:name"/>
  				<xsl:apply-templates select="spirit:envIdentifier"/>
      		<xsl:if test="not(spirit:hierarchyRef)">
     				<xsl:element name="ipxact:componentInstantiationRef"><xsl:value-of select="spirit:name"/></xsl:element>
      		</xsl:if>
      		<xsl:if test="spirit:hierarchyRef">
  		      <xsl:variable name="vendor" select="spirit:hierarchyRef/@spirit:vendor"/>
  		      <xsl:variable name="library" select="spirit:hierarchyRef/@spirit:library"/>
  		      <xsl:variable name="name" select="spirit:hierarchyRef/@spirit:name"/>
  		      <xsl:variable name="version" select="spirit:hierarchyRef/@spirit:version"/>
      		  <xsl:choose>
      		    <xsl:when test="$catalog">
      		      <xsl:choose>
      		        <xsl:when test="document($catalog)/ipxact:catalog/ipxact:designConfigurations/ipxact:ipxactFile/ipxact:vlnv[@vendor=$vendor and @library=$library and @name=$name and @version=$version]">
             				<xsl:element name="ipxact:designInstantiationRef"><xsl:value-of select="spirit:name"/>_design</xsl:element>
             				<xsl:element name="ipxact:designConfigurationInstantiationRef"><xsl:value-of select="spirit:name"/></xsl:element>
      		        </xsl:when>
      		        <xsl:when test="document($catalog)/ipxact:catalog/ipxact:designs/ipxact:ipxactFile/ipxact:vlnv[@vendor=$vendor and @library=$library and @name=$name and @version=$version]">
             				<xsl:element name="ipxact:designInstantiationRef"><xsl:value-of select="spirit:name"/></xsl:element>
      		        </xsl:when>
      		        <xsl:otherwise>
      		          <xsl:call-template name="create-default-instantiation-ref"/>
      		        </xsl:otherwise>
      		      </xsl:choose>
      		    </xsl:when>
      		    <xsl:otherwise>
   		          <xsl:call-template name="create-default-instantiation-ref"/>
      		    </xsl:otherwise>
      		  </xsl:choose>
      		</xsl:if>
    		</ipxact:view>
  		</xsl:for-each>
	  </ipxact:views>
	</xsl:template>

	<xsl:template name="create-default-instantiation-ref">
		<xsl:choose>
			<xsl:when test="$createDesignInstantiation">
				<xsl:element name="ipxact:designInstantiationRef">
					<xsl:value-of select="spirit:name"/>
				</xsl:element>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="ipxact:designConfigurationInstantiationRef">
					<xsl:value-of select="spirit:name"/>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="spirit:model/spirit:views">
		<ipxact:instantiations>
			<xsl:apply-templates select="spirit:view"/>
		</ipxact:instantiations>
	</xsl:template>
	<!-- component/abstractor: prevent modelParameters from coming out within a model -->
	<xsl:template match="spirit:model">
		<ipxact:model>
			<xsl:choose>
				<xsl:when test="spirit:views">
					<xsl:apply-templates select="spirit:views" mode="create-view-groups"/>
					<xsl:apply-templates select="spirit:views"/>
				</xsl:when>
				<xsl:otherwise>
					<!-- no-views but found modelParameters -->
					<xsl:if test="spirit:modelParameters">
						<ipxact:views>
							<ipxact:view>
								<ipxact:name>default</ipxact:name>
								<ipxact:componentInstantiationRef>default</ipxact:componentInstantiationRef>
							</ipxact:view>
						</ipxact:views>
						<ipxact:instantiations>
							<ipxact:componentInstantiation>
								<ipxact:name>default</ipxact:name>
								<xsl:apply-templates select="spirit:modelParameters"/>
							</ipxact:componentInstantiation>
						</ipxact:instantiations>
					</xsl:if>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:apply-templates select="spirit:ports"/>
		</ipxact:model>
	</xsl:template>
	<xsl:template match="spirit:modelParameters">
		<ipxact:moduleParameters>
			<xsl:apply-templates select="spirit:modelParameter"/>
		</ipxact:moduleParameters>
	</xsl:template>

	<!-- generatorChain: set apiType to TGI_2009 -->
	<xsl:template match="spirit:generatorChain/spirit:generator">
	  <ipxact:generator>
	    <xsl:apply-templates select="@*"/>
  	  <xsl:apply-templates select="spirit:name | spirit:displayName | spirit:description | spirit:phase | spirit:parameters"/>
  	  <ipxact:apiType>
    	  <xsl:choose>
    	    <xsl:when test="spirit:apiType='TGI'">TGI_2009</xsl:when>
    	    <xsl:when test="spirit:apiType='none'">none</xsl:when>
    	    <xsl:otherwise>TGI_2009</xsl:otherwise>
    	  </xsl:choose>
  	  </ipxact:apiType>
  	  <xsl:apply-templates select="spirit:transportMethods | spirit:generatorExe | spirit:vendorExtensions"/>
	  </ipxact:generator>
	</xsl:template>

	<!-- component generator: set apiType to TGI_2009 -->
	<xsl:template match="spirit:component/spirit:componentGenerators/spirit:componentGenerator">
	  <ipxact:componentGenerator>
	    <xsl:apply-templates select="@*"/>
  	  <xsl:apply-templates select="spirit:name | spirit:displayName | spirit:description | spirit:phase | spirit:parameters"/>
  	  <ipxact:apiType>
    	  <xsl:choose>
    	    <xsl:when test="spirit:apiType='TGI'">TGI_2009</xsl:when>
    	    <xsl:when test="spirit:apiType='none'">none</xsl:when>
    	    <xsl:otherwise>TGI_2009</xsl:otherwise>
    	  </xsl:choose>
  	  </ipxact:apiType>
  	  <xsl:apply-templates select="spirit:transportMethods | spirit:generatorExe | spirit:vendorExtensions | spirit:group"/>
	  </ipxact:componentGenerator>
	</xsl:template>

	<!-- designConfiguration: add lock element with value false -->
	<xsl:template match="spirit:designConfiguration/spirit:version">
		<xsl:apply-templates select="@spirit:version"/>
		<ipxact:version>
			<xsl:value-of select="."/>
		</ipxact:version>
	</xsl:template>
	<!-- design: add lock element with value false -->
	<xsl:template match="spirit:design/spirit:version">
		<xsl:apply-templates select="@spirit:version"/>
		<ipxact:version>
			<xsl:value-of select="."/>
		</ipxact:version>
	</xsl:template>
	<!-- Move <@spirit:{internalPortReference|externalPortReference}/spirit:left|spirit:right> to <spirit:partSelect>/<spirit:range>  -->
	<xsl:template match="spirit:internalPortReference|spirit:externalPortReference">
		<xsl:element name="ipxact:{local-name()}">
			<xsl:if test="@spirit:componentRef">
				<xsl:attribute name="componentRef"><xsl:value-of select="@spirit:componentRef"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@spirit:portRef">
				<xsl:attribute name="portRef"><xsl:value-of select="@spirit:portRef"/></xsl:attribute>
			</xsl:if>
			<xsl:if test="@spirit:left">
				<xsl:element name="ipxact:partSelect">
					<xsl:element name="ipxact:range">
						<xsl:element name="ipxact:left">
							<xsl:value-of select="@spirit:left"/>
						</xsl:element>
						<xsl:element name="ipxact:right">
							<xsl:value-of select="@spirit:right"/>
						</xsl:element>
					</xsl:element>
				</xsl:element>
			</xsl:if>
		</xsl:element>
	</xsl:template>
	<!-- Push constraintSetRef value into a localName sub-element  -->
	<xsl:template match="spirit:constraintSetRef">
		<ipxact:constraintSetRef>
			<ipxact:localName>
				<xsl:value-of select="."/>
			</ipxact:localName>
		</ipxact:constraintSetRef>
	</xsl:template>
	<!-- Push busInterfaceRef value into a localName sub-element  -->
	<xsl:template match="spirit:busInterfaceRef">
		<ipxact:busInterfaceRef>
			<ipxact:localName>
				<xsl:value-of select="."/>
			</ipxact:localName>
		</ipxact:busInterfaceRef>
	</xsl:template>
	<!-- Move <spirit:driver> to <spirit:drivers>/<spirit:driver>  -->
	<xsl:template match="spirit:model/spirit:ports/spirit:port/spirit:wire/spirit:driver">
		<xsl:element name="ipxact:drivers">
			<xsl:element name="ipxact:driver">
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates/>
			</xsl:element>
		</xsl:element>
	</xsl:template>
	<!-- Move <spirit:vector> to <spirit:partSelect/spirit:range> in busInterface references -->
	<xsl:template match="spirit:physicalPort/spirit:vector">
		<xsl:element name="ipxact:partSelect">
			<xsl:element name="ipxact:range">
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates/>
			</xsl:element>
		</xsl:element>
	</xsl:template>
	<xsl:template match="spirit:logicalPort/spirit:vector">
		<xsl:element name="ipxact:range">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>
	<!-- Move <spirit:vector> to <spirit:vectors>/<spirit:vector> in wire definitions -->
	<xsl:template match="spirit:wire/spirit:vector">
		<xsl:element name="ipxact:vectors">
			<xsl:element name="ipxact:vector">
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates/>
			</xsl:element>
		</xsl:element>
	</xsl:template>
	<!-- Move <spirit:abstractionType> to <spirit:abstractionTypes>/<spirit:abstractionType>  -->
	<xsl:template match="spirit:abstractionType">
		<xsl:element name="ipxact:abstractionTypes">
			<xsl:element name="ipxact:abstractionType">
				<ipxact:abstractionRef>
					<xsl:apply-templates select="@*"/>
				</ipxact:abstractionRef>
				<xsl:apply-templates select="../spirit:portMaps"/>
			</xsl:element>
		</xsl:element>
	</xsl:template>
	<!-- remove spirit:configurableElementValues -->
	<xsl:template match="spirit:configurableElementValues"/>
	<!-- move configurableElementValues -->
	<xsl:template match="spirit:configurableElementValues" mode="move-configurable-element-values">
		<ipxact:configurableElementValues>
			<xsl:apply-templates select="spirit:configurableElementValue"/>
		</ipxact:configurableElementValues>
	</xsl:template>
	<!-- Move configurableElementValues into componentRef -->
	<xsl:template match="spirit:componentRef">
		<xsl:element name="ipxact:componentRef">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="../spirit:configurableElementValues" mode="move-configurable-element-values"/>
		</xsl:element>
	</xsl:template>
	<!-- Move configurableElementValues into abstratorRef -->
	<xsl:template match="spirit:abstractorRef">
		<xsl:element name="ipxact:abstractorRef">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates select="../spirit:configurableElementValues" mode="move-configurable-element-values"/>
		</xsl:element>
	</xsl:template>

	<!-- move VLNV from generatorChainRef to generatorChainConfiguration -->
  <xsl:template match="spirit:designConfiguration/spirit:generatorChainConfiguration">
    <ipxact:generatorChainConfiguration>
		  <xsl:apply-templates select="spirit:generatorChainRef/@*"/>
      <xsl:apply-templates select="spirit:configurableElementValues"/>
    </ipxact:generatorChainConfiguration>
  </xsl:template>

	<xsl:template match="spirit:reset"/>

	<xsl:template match="spirit:viewNameRef">
		<ipxact:viewRef>
			<xsl:value-of select="."/>
		</ipxact:viewRef>
	</xsl:template>
	<xsl:template match="spirit:abstractor//spirit:viewNameRef">
		<ipxact:viewRef>
			<xsl:value-of select="."/>
		</ipxact:viewRef>
	</xsl:template>
	<!-- Handle transactional ports -->
	<xsl:template match="spirit:model/spirit:ports/spirit:port/spirit:transactional">
		<xsl:element name="ipxact:transactional">
			<xsl:apply-templates select="@*"/>
			<xsl:if test="spirit:service/spirit:initiative">
				<xsl:element name="ipxact:initiative">
					<xsl:value-of select="spirit:service/spirit:initiative"/>
				</xsl:element>
			</xsl:if>
			<xsl:if test="spirit:transTypeDef">
				<xsl:element name="ipxact:transTypeDefs">
					<xsl:element name="ipxact:transTypeDef">
						<xsl:apply-templates select="spirit:transTypeDef/spirit:typeName"/>
						<xsl:apply-templates select="spirit:transTypeDef/spirit:typeDefinition"/>
						<xsl:if test="spirit:transTypeDef/spirit:viewNameRef">
							<xsl:element name="ipxact:viewRef">
								<xsl:value-of select="spirit:transTypeDef/spirit:viewNameRef"/>
							</xsl:element>
						</xsl:if>
						<xsl:if test="spirit:service/spirit:serviceTypeDefs/spirit:serviceTypeDef">
							<xsl:element name="ipxact:typeParameters">
								<xsl:apply-templates select="spirit:service/spirit:serviceTypeDefs/spirit:serviceTypeDef"/>
							</xsl:element>
						</xsl:if>
						<!-- JMF Warning: spirit:service/spirit:vendorExtensions not converted ! -->
					</xsl:element>
				</xsl:element>
			</xsl:if>
			<xsl:if test="spirit:connection">
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates/>
			</xsl:if>
		</xsl:element>
	</xsl:template>
	<!-- Handle transactional port service parameters -->
	<xsl:template match="spirit:model/spirit:ports/spirit:port/spirit:transactional/spirit:service/spirit:serviceTypeDefs/spirit:serviceTypeDef/spirit:parameters">
		<xsl:element name="ipxact:typeParameters">
			<xsl:for-each select="spirit:parameter">
				<xsl:element name="ipxact:typeParameter">
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates select="*"/>
				</xsl:element>
			</xsl:for-each>
		</xsl:element>
	</xsl:template>
	<!-- Handle abstractionDefinition transactional ports -->
	<xsl:template match="spirit:abstractionDefinition/spirit:ports/spirit:port/spirit:transactional/spirit:onMaster">
		<xsl:element name="ipxact:onMaster">
			<xsl:call-template name="absdef_transactional_ports"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="spirit:abstractionDefinition/spirit:ports/spirit:port/spirit:transactional/spirit:onSlave">
		<xsl:element name="ipxact:onSlave">
			<xsl:call-template name="absdef_transactional_ports"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="spirit:abstractionDefinition/spirit:ports/spirit:port/spirit:transactional/spirit:onSystem">
		<xsl:element name="ipxact:onSystem">
			<xsl:if test="spirit:group">
				<xsl:apply-templates select="spirit:group"/>
			</xsl:if>
			<xsl:call-template name="absdef_transactional_ports"/>
		</xsl:element>
	</xsl:template>
	<xsl:template name="absdef_transactional_ports">
		<xsl:if test="spirit:presence">
			<xsl:element name="ipxact:presence">
				<xsl:value-of select="spirit:presence"/>
			</xsl:element>
		</xsl:if>
		<xsl:if test="spirit:service/spirit:initiative">
			<xsl:element name="ipxact:initiative">
				<xsl:value-of select="spirit:service/spirit:initiative"/>
			</xsl:element>
		</xsl:if>
		<xsl:if test="spirit:service/spirit:typeName">
			<xsl:element name="ipxact:protocol">
				<xsl:element name="ipxact:protocolType">
					<xsl:choose>
						<xsl:when test="spirit:service/spirit:typeName/@spirit:implicit='true'">tlm</xsl:when>
						<xsl:otherwise>
							<xsl:attribute name="custom"><xsl:value-of select="spirit:service/spirit:typeName"/></xsl:attribute>custom</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:element>
		</xsl:if>
	</xsl:template>

	<!-- Move ../<spirit:hierConnection> elements into <spirit:interconnections> -->
	<xsl:template match="spirit:componentInstances">
		<xsl:element name="ipxact:componentInstances">
			<xsl:apply-templates select="*"/>
		</xsl:element>
		<xsl:if test="not(../spirit:interconnections) and ../spirit:hierConnections">
			<xsl:element name="ipxact:interconnections">
				<xsl:apply-templates select="../spirit:hierConnections" mode="movehier"/>
			</xsl:element>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="spirit:interconnections">
		<xsl:element name="ipxact:interconnections">
			<xsl:apply-templates select="spirit:interconnection"/>
			<xsl:apply-templates select="../spirit:hierConnections" mode="movehier"/>
			<xsl:apply-templates select="spirit:monitorInterconnection"/>
		</xsl:element>
	</xsl:template>
	
	<xsl:template match="spirit:hierConnections" mode="movehier">
		<xsl:for-each select="spirit:hierConnection">
			<xsl:element name="ipxact:interconnection">
				<xsl:element name="ipxact:name">
					<xsl:value-of select="./@spirit:interfaceRef"/>
				</xsl:element>
				<xsl:for-each select="spirit:interface">
					<xsl:element name="ipxact:activeInterface">
						<xsl:apply-templates select="@*"/>
					</xsl:element>
				</xsl:for-each>
				<xsl:element name="ipxact:hierInterface">
					<xsl:attribute name="busRef"><xsl:value-of select="./@spirit:interfaceRef"/></xsl:attribute>
				</xsl:element>
				<xsl:apply-templates select="spirit:vendorExtensions"/>
			</xsl:element>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="spirit:design/spirit:hierConnections"/>

	<xsl:template match="spirit:port/spirit:access/spirit:portAccessHandle">
		<ipxact:accessHandles>
			<ipxact:accessHandle>
				<ipxact:slices>
					<ipxact:slice>
						<ipxact:pathSegments>
							<ipxact:pathSegment>
								<ipxact:pathSegmentName>
									<xsl:value-of select="."/>
								</ipxact:pathSegmentName>
							</ipxact:pathSegment>
						</ipxact:pathSegments>
					</ipxact:slice>
				</ipxact:slices>
			</ipxact:accessHandle>
		</ipxact:accessHandles>
	</xsl:template>
	<xsl:template match="spirit:whiteboxElementRef">
		<xsl:variable name="name" select="@spirit:name"/>
		<xsl:if test="not(/spirit:component/spirit:whiteboxElements/spirit:whiteboxElement[spirit:name=$name]/spirit:registerRef)">
			<ipxact:whiteboxElementRef>
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates select="*"/>
			</ipxact:whiteboxElementRef>
		</xsl:if>
	</xsl:template>
	<xsl:template match="spirit:whiteboxElements">
		<xsl:if test="count(spirit:whiteboxElement) > count(spirit:whiteboxElement/spirit:registerRef)">
			<ipxact:whiteboxElements>
				<xsl:apply-templates select="spirit:whiteboxElement"/>
			</ipxact:whiteboxElements>
		</xsl:if>
	</xsl:template>
	<xsl:template match="spirit:whiteboxElement">
		<xsl:variable name="whiteboxName" select="spirit:name"/>
		<xsl:choose>
			<xsl:when test="not(spirit:registerRef)">
				<ipxact:whiteboxElement>
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates select="*"/>
				</ipxact:whiteboxElement>
			</xsl:when>
			<xsl:when test="not(/spirit:component/spirit:model/spirit:views/spirit:view/spirit:whiteboxElementRefs/spirit:whiteboxElementRef[@spirit:name=$whiteboxName])">
				<xsl:call-template name="insertComment">
					<xsl:with-param name="number">1</xsl:with-param>
					<xsl:with-param name="message">Removing whiteboxElement '<xsl:value-of select="$whiteboxName"/>' without converting! No references could be found.</xsl:with-param>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="found">
					<xsl:variable name="registerRef" select="translate(spirit:registerRef, '/', '')"/>
					<xsl:for-each select="//spirit:register">
						<xsl:variable name="path">
							<xsl:for-each select="ancestor-or-self::*[spirit:name and not(self::spirit:component)]">
								<xsl:value-of select="spirit:name"/>
							</xsl:for-each>
						</xsl:variable>
						<xsl:if test="$registerRef=$path">found</xsl:if>
					</xsl:for-each>
				</xsl:variable>
				<xsl:if test="not(contains($found, 'found'))">
					<xsl:call-template name="insertComment">
						<xsl:with-param name="number">2</xsl:with-param>
						<xsl:with-param name="message">Removing whiteboxElement '<xsl:value-of select="$whiteboxName"/>' without converting! The registerRef '<xsl:value-of select="spirit:registerRef"/>' does not provide a path to a register.</xsl:with-param>
					</xsl:call-template>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="spirit:whiteboxPath">
		<ipxact:location>
			<ipxact:slice>
				<ipxact:pathSegments>
					<xsl:call-template name="split-path-into-segments">
						<xsl:with-param name="path" select="spirit:pathName/text()"/>
					</xsl:call-template>
				</ipxact:pathSegments>
				<xsl:if test="spirit:left">
					<ipxact:range>
						<ipxact:left>
							<xsl:value-of select="spirit:left"/>
						</ipxact:left>
						<ipxact:right>
							<xsl:value-of select="spirit:right"/>
						</ipxact:right>
					</ipxact:range>
				</xsl:if>
			</ipxact:slice>
		</ipxact:location>
	</xsl:template>
	<xsl:template match="spirit:userFileType">
		<ipxact:fileType user="{./text()}">user</ipxact:fileType>
	</xsl:template>
	<xsl:template name="split-path-into-segments">
		<xsl:param name="path"/>
		<xsl:choose>
			<!-- if the path contains the delimiter... -->
			<xsl:when test="contains($path, '/')">
				<ipxact:pathSegment>
					<ipxact:pathSegmentName>
						<xsl:value-of select="substring-before($path, '/')"/>
					</ipxact:pathSegmentName>
				</ipxact:pathSegment>
				<!-- call the template recursively... -->
				<xsl:call-template name="split-path-into-segments">
					<!-- with the path being the path after the delimiter -->
					<xsl:with-param name="path" select="substring-after($path, '/')"/>
				</xsl:call-template>
			</xsl:when>
			<!-- otherwise, create a segment with the path without a delimiter -->
			<xsl:otherwise>
				<ipxact:pathSegment>
					<ipxact:pathSegmentName>
						<xsl:value-of select="$path"/>
					</ipxact:pathSegmentName>
				</ipxact:pathSegment>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="spirit:viewConfiguration/spirit:viewName">
		<ipxact:view>
			<xsl:attribute name="viewRef"><xsl:value-of select="."/></xsl:attribute>
		</ipxact:view>
	</xsl:template>
	<xsl:template name="concat-path">
		<xsl:param name="path"/>
		<xsl:choose>
			<!-- if the path contains the delimiter... -->
			<xsl:when test="contains($path, '/')">
				<ipxact:pathSegment>
					<ipxact:pathSegmentName>
						<xsl:value-of select="substring-before($path, '/')"/>
					</ipxact:pathSegmentName>
				</ipxact:pathSegment>
				<!-- call the template recursively... -->
				<xsl:call-template name="split-path-into-segments">
					<!-- with the path being the path after the delimiter -->
					<xsl:with-param name="path" select="substring-after($path, '/')"/>
				</xsl:call-template>
			</xsl:when>
			<!-- otherwise, create a segment with the path without a delimiter -->
			<xsl:otherwise>
				<ipxact:pathSegment>
					<ipxact:pathSegmentName>
						<xsl:value-of select="$path"/>
					</ipxact:pathSegmentName>
				</ipxact:pathSegment>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="spirit:remapPort">
		<ipxact:remapPort>
			<xsl:attribute name="portRef"><xsl:value-of select="@spirit:portNameRef"/></xsl:attribute>
			<xsl:if test="@spirit:portIndex">
				<ipxact:portIndex>
					<xsl:value-of select="@spirit:portIndex"/>
				</ipxact:portIndex>
			</xsl:if>
			<ipxact:value>
				<xsl:call-template name="parse-scale">
					<xsl:with-param name="value" select="normalize-space(.)"/>
				</xsl:call-template>
			</ipxact:value>
		</ipxact:remapPort>
	</xsl:template>
	<xsl:template match="@spirit:id">
		<xsl:attribute name="xml:id"><xsl:value-of select="."/></xsl:attribute>
	</xsl:template>
	<xsl:template name="write-parameters">
		<xsl:param name="params" select="."/>
		<xsl:if test="$debug">
			<xsl:message>write-parameters</xsl:message>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="function-available('msxsl:node-set')">
				<xsl:if test="$debug">
					<xsl:message>msxml</xsl:message>
				</xsl:if>
				<xsl:if test="count(msxsl:node-set($params)/*) > 0">
					<ipxact:parameters>
						<xsl:copy-of select="msxsl:node-set($params)/*"/>
					</ipxact:parameters>
				</xsl:if>
			</xsl:when>
			<xsl:when test="function-available('exslt:node-set')">
				<xsl:if test="$debug">
					<xsl:message>exslt</xsl:message>
				</xsl:if>
				<xsl:if test="count(exslt:node-set($params)/*) > 0">
					<ipxact:parameters>
						<xsl:copy-of select="exslt:node-set($params)/*"/>
					</ipxact:parameters>
				</xsl:if>
			</xsl:when>
			<xsl:when test="function-available('xalan:nodeset')">
				<xsl:if test="$debug">
					<xsl:message>xalan</xsl:message>
				</xsl:if>
				<xsl:if test="count(xalan:nodeset($params)/*) > 0">
					<ipxact:parameters>
						<xsl:copy-of select="xalan:nodeset($params)/*"/>
					</ipxact:parameters>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<xsl:if test="$debug">
					<xsl:message>other</xsl:message>
				</xsl:if>
				<xsl:if test="count($params/*) > 0">
					<ipxact:parameters>
						<xsl:copy-of select="$params/*"/>
					</ipxact:parameters>
				</xsl:if>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="parse-expression">
		<xsl:param name="value" select="."/>
		<xsl:if test="$debug">
			<xsl:message>parse-expression(<xsl:value-of select="$value"/>)</xsl:message>
		</xsl:if>
		<xsl:variable name="result">
			<xsl:choose>
				<xsl:when test="function-available('msxsl:node-set')">
					<xsl:if test="$debug">
						<xsl:message>msxml</xsl:message>
					</xsl:if>
					<xsl:call-template name="msxsl:parse">
						<xsl:with-param name="value" select="normalize-space($value)"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="function-available('exslt:node-set')">
					<xsl:if test="$debug">
						<xsl:message>exslt</xsl:message>
					</xsl:if>
					<xsl:call-template name="exslt:parse">
						<xsl:with-param name="value" select="normalize-space($value)"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="function-available('xalan:nodeset')">
					<xsl:if test="$debug">
						<xsl:message>xalan</xsl:message>
					</xsl:if>
					<xsl:call-template name="xalan:parse">
						<xsl:with-param name="value" select="normalize-space($value)"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:otherwise>
					<xsl:if test="$debug">
						<xsl:message>other</xsl:message>
					</xsl:if>
					<xsl:call-template name="parse">
						<xsl:with-param name="value" select="normalize-space($value)"/>
					</xsl:call-template>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="normalize-space($result)"/>
	</xsl:template>
</xsl:stylesheet>
